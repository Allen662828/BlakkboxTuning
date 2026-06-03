# Improved heuristic-based map finder for DENSO BINs
# - Detects candidate 1D and 2D maps for multiple element sizes (8/16/32-bit)
# - Infers possible shapes for 2D maps by testing row similarity and smoothness
# - Uses numpy for efficient scanning

import os
import numpy as np
from typing import List, Dict, Tuple


def _read_region(path: str, offset: int, length: int) -> bytes:
    with open(path, "rb") as f:
        f.seek(offset)
        return f.read(length)


def _smoothness_score(arr: np.ndarray) -> float:
    # Lower score = smoother. Use normalized mean absolute second difference.
    if arr.size < 3:
        return 1.0
    dif2 = np.abs(np.diff(arr, n=2)).astype(np.float64)
    score = np.mean(dif2) / (np.max(np.abs(arr)) + 1e-9)
    return float(score)


def _monotonic_fraction(arr: np.ndarray) -> float:
    if arr.size < 2:
        return 1.0
    dif = np.diff(arr)
    return float(np.mean(dif >= 0) if np.mean(dif >= 0) >= 0.5 else np.mean(dif <= 0))


def infer_2d_shapes(length_bytes: int, bytes_per_cell: int, max_width: int = 512) -> List[Tuple[int,int]]:
    # Given region length in bytes and cell size, return plausible (rows, cols)
    cells = length_bytes // bytes_per_cell
    shapes = []
    # Limit potential column counts to divisors up to max_width
    for cols in range(2, min(cells, max_width) + 1):
        if cells % cols == 0:
            rows = cells // cols
            if rows >= 2:
                shapes.append((rows, cols))
    return shapes


def test_shape_similarity(region: bytes, rows: int, cols: int, bytes_per_cell: int, dtype) -> float:
    # Interpret region as rows x cols array and compute row-to-row correlation / similarity score
    arr = np.frombuffer(region, dtype=dtype)
    if arr.size != rows * cols:
        return 0.0
    grid = arr.reshape((rows, cols))
    # compute normalized pairwise row differences mean
    diffs = np.mean(np.abs(np.diff(grid.astype(np.float64), axis=0)), axis=1)
    score = 1.0 / (1.0 + np.mean(diffs))
    return float(score)


def scan_for_maps(path: str,
                  min_cells: int = 16,
                  window_bytes: int = 4096,
                  step_bytes: int = 2048,
                  value_sizes: List[int] = [2, 1],
                  max_shape_width: int = 256) -> List[Dict]:
    """Scan the BIN for candidate 1D/2D maps.

    Returns a list of candidates with fields:
      - offset, length_bytes, bytes_per_cell, dtype, confidence, suggested_shapes [(rows,cols,shape_score)],
      - 1D characteristics: monotonic_fraction, smoothness
    """
    filesize = os.path.getsize(path)
    candidates = []

    # sliding windows across file
    with open(path, "rb") as f:
        for offset in range(0, max(1, filesize - min(window_bytes, filesize)) + 1, step_bytes):
            length = min(window_bytes, filesize - offset)
            region = f.read(length)
            if len(region) < min_cells * min(value_sizes):
                continue
            # Try different element widths
            for bpc in value_sizes:
                # must have whole cells
                cells = len(region) // bpc
                if cells < min_cells:
                    continue
                # select numpy dtype
                if bpc == 1:
                    dtype = np.uint8
                elif bpc == 2:
                    dtype = np.uint16
                elif bpc == 4:
                    dtype = np.uint32
                else:
                    continue
                arr = np.frombuffer(region[:cells * bpc], dtype=dtype)
                # compute simple metrics
                smooth = _smoothness_score(arr.flatten())
                mono = _monotonic_fraction(arr.flatten())
                # candidate heuristics: smoothness small and some monotonicity
                # score combines smoothness and monotonicity and low entropy proxy
                score = (1.0 / (1.0 + smooth)) * (0.5 + 0.5 * mono)
                # Try to infer 2D shapes and test similarity
                shapes = []
                inferred = infer_2d_shapes(len(arr) * bpc, bpc, max_width=max_shape_width)
                for (r, c) in inferred:
                    s = test_shape_similarity(region[:r * c * bpc], r, c, bpc, dtype)
                    if s > 0.02:
                        shapes.append((r, c, s))
                # keep candidate if score and/or shapes look promising
                if score > 0.12 or len(shapes) > 0:
                    candidates.append({
                        "offset": offset,
                        "length_bytes": len(arr) * bpc,
                        "bytes_per_cell": bpc,
                        "dtype": str(dtype),
                        "smoothness": float(smooth),
                        "monotonic_fraction": float(mono),
                        "confidence": float(score),
                        "suggested_shapes": sorted(shapes, key=lambda x: -x[2])
                    })
            # reset file pointer for next window start
            f.seek(offset + step_bytes)
    # deduplicate overlapping candidates favoring higher confidence
    candidates_sorted = sorted(candidates, key=lambda c: (-c["confidence"], c["offset"]))
    dedup = []
    occupied = []
    for c in candidates_sorted:
        o1 = c["offset"]
        o2 = c["offset"] + c["length_bytes"]
        overlap = False
        for (a,b) in occupied:
            if not (o2 <= a or o1 >= b):
                overlap = True
                break
        if not overlap:
            dedup.append(c)
            occupied.append((o1,o2))
    return dedup


if __name__ == "__main__":
    import argparse, json
    p = argparse.ArgumentParser()
    p.add_argument('bin')
    p.add_argument('-o','--out')
    args = p.parse_args()
    res = scan_for_maps(args.bin)
    if args.out:
        with open(args.out,'w') as f:
            json.dump(res, f, indent=2)
    else:
        import pprint
        pprint.pprint(res)
