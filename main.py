import os
import shutil
import sys
from pathlib import Path

CEILING = 20
TAG = "wifi-one-word"
OUT_NAME = "entry.txt"  # fixed artifact name the scorer expects

def measure(txt):
    words = txt.split()
    return len(txt), len(words)

def run():
    src = Path(__file__).resolve().parent / "entry.txt"
    blob = src.read_text(encoding="utf-8").strip()
    size, count = measure(blob)
    ok = bool(blob) and 0 < size <= CEILING and count == 1
    verdict = {"tag": TAG, "size": size, "count": count, "text": blob,
               "verdict": "pass" if ok else "reject"}
    return verdict, ok

def emit(ok):
    if not ok:
        return
    dest_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path(__file__).resolve().parent / "entry.txt", dest_dir / OUT_NAME)

verdict, ok = run()
emit(ok)
import json
print(json.dumps(verdict, ensure_ascii=False))
sys.exit(0 if ok else 1)
