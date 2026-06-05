from pathlib import Path

class BinComparator:
    def __init__(self, original_path, mod_path):
        self.original_path = Path(original_path)
        self.mod_path = Path(mod_path)

    def load_bins(self):
        self.original = self.original_path.read_bytes()
        self.mod = self.mod_path.read_bytes()

    def compare(self):
        if len(self.original) != len(self.mod):
            raise ValueError('BIN size mismatch')

        changes = []

        for addr, (o, m) in enumerate(zip(self.original, self.mod)):
            if o != m:
                changes.append({
                    'address': hex(addr),
                    'original': o,
                    'modified': m,
                    'delta': m - o
                })

        return changes
