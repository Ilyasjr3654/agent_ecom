"""Acquire pinned public sources and build the PFA43 data pack (stdlib only)."""
import argparse
import csv
import gzip
import hashlib
import io
import json
import re
import shutil
import urllib.request
import zipfile
from contextlib import ExitStack
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRANDS = {"AmazonHelp", "AskeBay", "AskTarget", "Walmart", "ArgosHelpers",
          "NikeSupport", "NeweggService", "marksandspencer"}


def sha(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def gzip_bytes(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f, gzip.GzipFile(filename="", fileobj=f, mode="wb", mtime=0) as g:
        g.write(data)


def acquire(cache):
    cache.mkdir(parents=True, exist_ok=True)
    lock = json.loads((ROOT / "data/sources.lock.json").read_text())
    for name, spec in lock.items():
        dest = cache / name
        if not dest.exists():
            tmp = dest.with_suffix(dest.suffix + ".part")
            print("Downloading", name, flush=True)
            with urllib.request.urlopen(spec["url"], timeout=120) as r, tmp.open("wb") as f:
                shutil.copyfileobj(r, f)
            if sha(tmp) != spec["sha256"]:
                tmp.unlink()
                raise ValueError(f"Source checksum mismatch: {name}")
            tmp.replace(dest)
        if sha(dest) != spec["sha256"]:
            raise ValueError(f"Cached source checksum mismatch: {name}")


def prepare_abcd(cache):
    out = ROOT / "data/raw/abcd"
    out.mkdir(parents=True, exist_ok=True)
    for name in ("abcd_v1.1.json.gz", "guidelines.json", "kb.json", "ontology.json"):
        shutil.copyfile(cache / name, out / name)
    gzip_bytes(out / "utterances.json.gz", (cache / "utterances.json").read_bytes())
    shutil.copyfile(cache / "ABCD_LICENSE", out / "LICENSE")
    with gzip.open(out / "abcd_v1.1.json.gz", "rt", encoding="utf-8") as f:
        data = json.load(f)
    ids = [set(c["convo_id"] for c in rows) for rows in data.values()]
    assert sum(map(len, ids)) == len(set.union(*ids)), "ABCD split overlap"
    return {s: len(rows) for s, rows in data.items()}


def prepare_olist(cache):
    # All relational tables, excluding the large optional geolocation table.
    counts, ids = {}, {}
    with zipfile.ZipFile(cache / "olist.zip") as z:
        for name in z.namelist():
            if "geolocation" in name:
                continue
            payload = z.read(name)
            rows = list(csv.DictReader(io.StringIO(payload.decode("utf-8"))))
            counts[name] = len(rows)
            if "orders_dataset" in name:
                ids["orders"] = {r["order_id"] for r in rows}
                ids["order_customers"] = {r["customer_id"] for r in rows}
            if "customers_dataset" in name:
                ids["customers"] = {r["customer_id"] for r in rows}
            if "products_dataset" in name:
                ids["products"] = {r["product_id"] for r in rows}
            if "order_items" in name:
                ids["item_orders"] = {r["order_id"] for r in rows}
                ids["item_products"] = {r["product_id"] for r in rows}
            if "order_payments" in name or "order_reviews" in name:
                ids[name] = {r["order_id"] for r in rows}
            gzip_bytes(ROOT / "data/raw/olist" / (name + ".gz"), payload)
    assert ids["order_customers"] <= ids["customers"]
    assert ids["item_orders"] <= ids["orders"]
    assert ids["item_products"] <= ids["products"]
    for key in ("olist_order_payments_dataset.csv", "olist_order_reviews_dataset.csv"):
        assert ids[key] <= ids["orders"]
    return counts


def prepare_twitter(cache, limit):
    # Connected components retain every available branch of the selected threads.
    # Missing tweets in the original source cannot be reconstructed.
    parent, seeds = {}, set()

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        a, b = find(x), find(y)
        if a != b:
            parent[max(a, b)] = min(a, b)

    def rows(z):
        with z.open("twcs/twcs.csv") as f:
            yield from csv.DictReader(io.TextIOWrapper(f, encoding="utf-8"))

    with zipfile.ZipFile(cache / "twitter.zip") as z:
        for r in rows(z):
            tid = int(r["tweet_id"])
            find(tid)
            for field in ("in_response_to_tweet_id", "response_tweet_id"):
                for ref in r[field].split(","):
                    if ref.strip():
                        union(tid, int(ref))
            if r["author_id"] in BRANDS and r["inbound"].lower() == "false":
                seeds.add(tid)
        candidates = {find(t) for t in seeds}
        ranked = sorted(candidates, key=lambda t: hashlib.sha256(f"42:{t}".encode()).digest())
        selected = ranked[:limit]
        n = len(selected)
        split_for = {cid: ("train" if i < int(n * .70) else "validation" if i < int(n * .85) else "test")
                     for i, cid in enumerate(selected)}
        stats = {s: {"threads": list(split_for.values()).count(s), "tweets": 0}
                 for s in ("train", "validation", "test")}
        out = ROOT / "data/processed/twitter"
        out.mkdir(parents=True, exist_ok=True)
        with ExitStack() as stack:
            writers = {}
            for split in stats:
                f = stack.enter_context((out / f"{split}.jsonl.gz").open("wb"))
                writers[split] = stack.enter_context(gzip.GzipFile(filename="", fileobj=f, mode="wb", mtime=0))
            for r in rows(z):
                cid = find(int(r["tweet_id"]))
                if cid not in split_for:
                    continue
                split = split_for[cid]
                r["conversation_id"] = str(cid)
                # Source already pseudonymizes handles; mask residual emails and URLs.
                r["text"] = re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[EMAIL]", r["text"])
                r["text"] = re.sub(r"https?://\S+", "[URL]", r["text"])
                writers[split].write((json.dumps(r, ensure_ascii=False) + "\n").encode())
                stats[split]["tweets"] += 1
    return {"brands": sorted(BRANDS), "eligible_threads": len(candidates), "splits": stats,
            "split_method": "connected components; SHA256(42:component_id), 70/15/15",
            "limitations": "No intent annotations; source may omit tweets. Semantic near-duplicates and remaining personal data need review before model training."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", type=Path, default=ROOT / ".cache/datasets")
    parser.add_argument("--twitter-threads", type=int, default=10000)
    args = parser.parse_args()
    if args.twitter_threads <= 0:
        parser.error("--twitter-threads must be positive")
    acquire(args.cache)
    stats = {"abcd": prepare_abcd(args.cache), "olist": prepare_olist(args.cache),
             "twitter": prepare_twitter(args.cache, args.twitter_threads)}
    files = {}
    for directory in (ROOT / "data/raw", ROOT / "data/processed"):
        for p in sorted(directory.rglob("*")):
            if p.is_file():
                assert p.stat().st_size < 95_000_000, f"Too large for Git: {p}"
                files[str(p.relative_to(ROOT))] = {"sha256": sha(p), "bytes": p.stat().st_size}
    manifest = {"acquired_on": "2026-11-20", "statistics": stats, "files": files,
                "amazon": {"status": "not_redistributed", "reason": "No explicit data redistribution license from publisher", "source": "https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023"}}
    (ROOT / "data/manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(stats, indent=2), flush=True)


if __name__ == "__main__":
    main()
