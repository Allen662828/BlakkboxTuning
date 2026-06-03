# Simple heuristic-based map finder for DENSO BINs
import struct


def scan_for_16bit_tables(path, min_cells=8, max_stride=1024):
    """Scan for regions that look like 16-bit value arrays with repeated structure.
    Returns list of (offset, length, stride_guess)
    """
    results = []
    with open(path, "rb") as f:
        data = f.read()
    n = len(data)
    # look for sequences where values change smoothly
    i = 0
    while i + 2 * min_cells <= n:
        # try a window
        window = data[i:i + 2 * min_cells]
        vals = struct.unpack("<%dH" % min_cells, window)
        diffs = [abs(vals[j+1]-vals[j]) for j in range(len(vals)-1)]
        avg_diff = sum(diffs)/len(diffs)
        if avg_diff <= 500:  # heuristic threshold
            # try to grow
            j = i + 2 * min_cells
            while j + 2 <= n:
                v = struct.unpack_from("<H", data, j)[0]
                # check if similar progression
                j += 2
            # record candidate region (simple: record min_cells*2)
            results.append({"offset": i, "length": 2*min_cells, "stride": 2})
            i += 2*min_cells
        else:
            i += 2
    return results

if __name__ == "__main__":
    import argparse, json
    p = argparse.ArgumentParser()
    p.add_argument("bin")
    p.add_argument("-o", "--out")
    args = p.parse_args()
    res = scan_for_16bit_tables(args.bin)
    if args.out:
        with open(args.out, "w") as f:
            json.dump(res, f, indent=2)
    else:
        print(res)
