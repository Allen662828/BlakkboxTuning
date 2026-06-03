# Minimal BIN analyzer for DENSO ECU BINs
import os
import re
import mmap
import hashlib
import math
from collections import Counter

ASCII_RE = re.compile(rb"[ -~]{4,}")


def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def file_size(path):
    return os.path.getsize(path)


def entropy(data):
    if not data:
        return 0.0
    counts = Counter(data)
    entropy = 0.0
    for c in counts.values():
        p = c / len(data)
        entropy -= p * math.log2(p)
    return entropy


def sliding_entropy(path, window=4096, step=2048, max_windows=256):
    sizes = []
    with open(path, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        n = mm.size()
        count = 0
        for off in range(0, n, step):
            if count >= max_windows:
                break
            end = min(off + window, n)
            sizes.append((off, entropy(mm[off:end])))
            count += 1
        mm.close()
    return sizes


def extract_ascii_strings(path, min_len=4):
    results = []
    with open(path, "rb") as f:
        data = f.read()
    for m in ASCII_RE.finditer(data):
        s = m.group(0).decode("ascii", errors="ignore")
        if len(s) >= min_len:
            results.append((m.start(), s))
    return results


def find_swid_candidates(strings):
    # crude: look for typical SWID patterns like "SWID", "SW_", or long alnum blocks
    candidates = []
    for off, s in strings:
        if "SWID" in s or "SW_" in s or re.search(r"[A-Z0-9]{6,}", s):
            candidates.append((off, s))
    return candidates


def checksum_candidates(path):
    # naive: find 2-byte and 4-byte little-endian sums over small regions
    # returns empty list as placeholder for later expansion
    return []


def analyze_bin(path):
    out = {}
    out["path"] = path
    out["sha256"] = sha256_of_file(path)
    out["size"] = file_size(path)
    out["entropy_windows"] = sliding_entropy(path)
    strings = extract_ascii_strings(path)
    out["ascii_strings"] = strings[:200]
    out["swid_candidates"] = find_swid_candidates(strings)
    out["checksum_candidates"] = checksum_candidates(path)
    return out

if __name__ == "__main__":
    import argparse
    import json
    p = argparse.ArgumentParser()
    p.add_argument("bin", help="Path to BIN file")
    p.add_argument("-o", "--out", help="Write JSON summary to file")
    args = p.parse_args()
    res = analyze_bin(args.bin)
    if args.out:
        with open(args.out, "w") as f:
            json.dump(res, f, indent=2)
    else:
        import pprint
        pprint.pprint(res)
