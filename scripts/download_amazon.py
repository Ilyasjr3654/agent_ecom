"""Download original All_Beauty files locally, outside versioned data."""
import argparse
import hashlib
import json
import shutil
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata-only", action="store_true", help="Download product metadata only")
    args = parser.parse_args()
    out = ROOT / "data/local/amazon"
    out.mkdir(parents=True, exist_ok=True)
    api = "https://huggingface.co/api/datasets/McAuley-Lab/Amazon-Reviews-2023"
    with urllib.request.urlopen(api, timeout=60) as response:
        revision = json.load(response)["sha"]
    files = ["raw/meta_categories/meta_All_Beauty.jsonl"]
    if not args.metadata_only:
        files.append("raw/review_categories/All_Beauty.jsonl")
    manifest = {"repository": "McAuley-Lab/Amazon-Reviews-2023", "revision": revision, "files": []}
    for name in files:
        url = f"https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/resolve/{revision}/{name}?download=true"
        dest = out / Path(name).name
        tmp = dest.with_suffix(dest.suffix + ".part")
        print("Downloading", dest.name, flush=True)
        with urllib.request.urlopen(url, timeout=180) as response, tmp.open("wb") as f:
            shutil.copyfileobj(response, f)
        with tmp.open("rb") as f:
            digest = hashlib.file_digest(f, "sha256").hexdigest()
        tmp.replace(dest)
        manifest["files"].append({"file": dest.name, "url": url, "sha256": digest, "bytes": dest.stat().st_size})
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("Local files ready. Join reviews and metadata by parent_asin; this script does not publish them.")


if __name__ == "__main__":
    main()
