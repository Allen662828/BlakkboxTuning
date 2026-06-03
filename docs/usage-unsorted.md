# Usage for Unsorted Data Ingest

This document explains the minimal usage for the Unsorted Data Ingest library added to the backend.

- Ingest a single file:
  python tools/cli_ingest.py ingest --file ./evidence/log1.txt --db data/attachments.db --link-bin <BIN_SHA256>

- Ingest a folder recursively:
  python tools/cli_ingest.py ingest --dir ./evidence --db data/attachments.db

- Search extracted text:
  python tools/cli_ingest.py search --query "rail pressure" --db data/attachments.db

Notes:
- OCR is optional and disabled by default. Enable with --ocr (requires Tesseract installed on host).
- Attachments DB is SQLite and created at the path you provide (default data/attachments.db).
- Thumbnails are stored in the DB; extracted text is stored in an FTS5 virtual table for fast search.
