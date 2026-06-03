"""Simple SQLite storage with FTS5 for attachments."""
import os
import sqlite3
import hashlib
import time

SCHEMA = [
    "CREATE TABLE IF NOT EXISTS attachments (id INTEGER PRIMARY KEY, sha256 TEXT UNIQUE, filename TEXT, mime TEXT, size INTEGER, extracted_text TEXT, ingestion_ts INTEGER)",
    "CREATE TABLE IF NOT EXISTS thumbnails (attachment_id INTEGER PRIMARY KEY, png BLOB)",
    "CREATE TABLE IF NOT EXISTS attachment_bins (attachment_id INTEGER, bin_sha256 TEXT, PRIMARY KEY (attachment_id, bin_sha256))",
    # FTS5 virtual table for full-text search
    "CREATE VIRTUAL TABLE IF NOT EXISTS fts_attachments USING fts5(extracted_text, content='attachments', content_rowid='id')"
]


class AttachmentStore:
    def __init__(self, db_path="data/attachments.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self._init()

    def _init(self):
        cur = self.conn.cursor()
        for s in SCHEMA:
            cur.execute(s)
        self.conn.commit()

    def _sha256(self, path):
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def insert_attachment(self, path, mime, size, extracted_text):
        sha = self._sha256(path)
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM attachments WHERE sha256=?", (sha,))
        row = cur.fetchone()
        if row:
            return row[0]
        ts = int(time.time())
        cur.execute("INSERT INTO attachments (sha256, filename, mime, size, extracted_text, ingestion_ts) VALUES (?,?,?,?,?,?)",
                    (sha, os.path.basename(path), mime, size, extracted_text, ts))
        aid = cur.lastrowid
        # insert into FTS table
        cur.execute("INSERT INTO fts_attachments(rowid, extracted_text) VALUES (?,?)", (aid, extracted_text or ""))
        self.conn.commit()
        return aid

    def store_thumbnail(self, attachment_id, png_bytes):
        cur = self.conn.cursor()
        cur.execute("INSERT OR REPLACE INTO thumbnails (attachment_id, png) VALUES (?,?)", (attachment_id, png_bytes))
        self.conn.commit()

    def link_to_bin(self, attachment_id, bin_sha256):
        cur = self.conn.cursor()
        cur.execute("INSERT OR IGNORE INTO attachment_bins (attachment_id, bin_sha256) VALUES (?,?)", (attachment_id, bin_sha256))
        self.conn.commit()

    def search_text(self, query, limit=20):
        cur = self.conn.cursor()
        cur.execute("SELECT attachments.id, filename, mime, snippets(fts_attachments, 0, '...', '...', '...', 10) FROM fts_attachments JOIN attachments ON fts_attachments.rowid=attachments.id WHERE fts_attachments MATCH ? LIMIT ?", (query, limit))
        return cur.fetchall()

    def get_sha_for_id(self, attachment_id):
        cur = self.conn.cursor()
        cur.execute("SELECT sha256 FROM attachments WHERE id=?", (attachment_id,))
        r = cur.fetchone()
        return r[0] if r else None

