from __future__ import annotations

import re


class SWIDDetector:
    KNOWN_PREFIXES = [
        '89663',
        '89661',
        '1860',
        'MEC',
        'CSTMR',
        'SW#',
    ]

    ASCII_RE = re.compile(rb'[ -~]{6,}')
    SWID_RE = re.compile(rb'(?:\b(?:SW#)?[A-Z0-9]{4,}(?:-[A-Z0-9]{4,})+\b|\b[A-Z0-9]{12,}\b)')

    def _candidates_from_bytes(self, data: bytes) -> list[str]:
        candidates: list[str] = []
        for match in self.ASCII_RE.finditer(data):
            text = match.group(0).decode('ascii', errors='ignore').strip()
            if self.SWID_RE.search(match.group(0)) or any(token in text for token in self.KNOWN_PREFIXES):
                candidates.append(text)
        return candidates

    def detect(self, filename, data: bytes | None = None):
        filename_text = str(filename or '')
        for prefix in self.KNOWN_PREFIXES:
            if prefix in filename_text:
                return {
                    'detected': True,
                    'sw_family': prefix,
                    'sw_id': filename_text,
                    'candidates': [filename_text],
                }

        candidates: list[str] = []
        if data:
            candidates = self._candidates_from_bytes(data)
            if candidates:
                return {
                    'detected': True,
                    'sw_family': 'denso',
                    'sw_id': candidates[0],
                    'candidates': candidates[:10],
                }

        return {
            'detected': False,
            'sw_family': None,
            'sw_id': None,
            'candidates': candidates,
        }
