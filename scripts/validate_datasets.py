"""Validate data checksums, counts and conversation-level split isolation."""
import csv
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    m = json.loads((ROOT / "data/manifest.json").read_text())
    for name, spec in m["files"].items():
        p = ROOT / name
        assert p.stat().st_size == spec["bytes"], name
        with p.open("rb") as f:
            assert hashlib.file_digest(f, "sha256").hexdigest() == spec["sha256"], name
    for name, count in m["statistics"]["olist"].items():
        with gzip.open(ROOT / "data/raw/olist" / (name + ".gz"), "rt", encoding="utf-8", newline="") as f:
            assert sum(1 for _ in csv.DictReader(f)) == count, name
    seen_threads, seen_tweets = set(), set()
    for split, expected in m["statistics"]["twitter"]["splits"].items():
        threads, count = set(), 0
        with gzip.open(ROOT / "data/processed/twitter" / (split + ".jsonl.gz"), "rt", encoding="utf-8") as f:
            for line in f:
                row = json.loads(line)
                assert row["tweet_id"] not in seen_tweets
                seen_tweets.add(row["tweet_id"])
                threads.add(row["conversation_id"])
                count += 1
        assert not seen_threads.intersection(threads), "Conversation split leakage"
        seen_threads.update(threads)
        assert count == expected["tweets"] and len(threads) == expected["threads"]
    with gzip.open(ROOT / "data/raw/abcd/abcd_v1.1.json.gz", "rt", encoding="utf-8") as f:
        abcd = json.load(f)
    seen = set()
    for split, rows in abcd.items():
        ids = {r["convo_id"] for r in rows}
        assert len(ids) == len(rows) == m["statistics"]["abcd"][split]
        assert not seen.intersection(ids), "ABCD split leakage"
        seen.update(ids)
    print(f"OK: {len(m['files'])} files verified; Olist counts; ABCD and Twitter split isolation.")


if __name__ == "__main__":
    main()
