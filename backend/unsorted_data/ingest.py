"""Unsorted data ingestion orchestrator
Provides ingest_file and ingest_folder functions that parse files and store metadata in SQLite.
"""
import os
from .parsers import detect_mime, extract_text, generate_thumbnail
from .storage import AttachmentStore


def ingest_file(path, link_to_bin=None, ocr=False, db_path="data/attachments.db", max_size=50*1024*1024):
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    size = os.path.getsize(path)
    if size > max_size:
        return {"skipped": True, "reason": "file too large", "path": path}
    mime = detect_mime(path)
    text = extract_text(path, ocr=ocr)
    thumb = generate_thumbnail(path)
    store = AttachmentStore(db_path)
    att_id = store.insert_attachment(path, mime, size, text)
    if thumb:
        store.store_thumbnail(att_id, thumb)
    if link_to_bin:
        store.link_to_bin(att_id, link_to_bin)
    return {"id": att_id, "sha": store.get_sha_for_id(att_id), "mime": mime}


def ingest_folder(folder, pattern=None, **kwargs):
    import glob
    files = []
    if pattern:
        globp = os.path.join(folder, pattern)
    else:
        globp = os.path.join(folder, "**/*")
    for p in glob.glob(globp, recursive=True):
        if os.path.isfile(p):
            try:
                r = ingest_file(p, **kwargs)
                files.append((p, r))
            except Exception as e:
                files.append((p, {"error": str(e)}))
    return files
