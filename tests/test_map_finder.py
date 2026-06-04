import os
import tempfile
import numpy as np
from backend.ecu_tools.map_finder import scan_for_maps


def test_detect_synthetic_uint16_grid():
    # create a synthetic 1D/2D map: 16 rows x 32 cols of uint16 with smooth gradients
    rows, cols = 16, 32
    grid = np.zeros((rows, cols), dtype=np.uint16)
    for r in range(rows):
        for c in range(cols):
            grid[r, c] = (r * 10 + c * 2) & 0xFFFF
    data = grid.tobytes()

    tmpdir = tempfile.mkdtemp()
    path = os.path.join(tmpdir, 'synthetic.bin')
    with open(path, 'wb') as f:
        f.write(b'HEADER1234')
        f.write(data)
        f.write(b'TAIL')

    res = scan_for_maps(path, window_bytes=4096, step_bytes=512, min_cells=32, value_sizes=[2])
    # we expect at least one candidate overlapping the region after header
    assert any(r['offset'] > 0 and r['bytes_per_cell']==2 for r in res)

