import os
import tempfile
from backend.unsorted_data.ingest import ingest_file
from backend.unsorted_data.storage import AttachmentStore


def test_ingest_text_file():
    tmpdir = tempfile.mkdtemp()
    txt = os.path.join(tmpdir, 'sample.txt')
    with open(txt, 'w') as f:
        f.write('rail pressure error 0x1A\nSome diagnostic log')
    db = os.path.join(tmpdir, 'attachments.db')
    res = ingest_file(txt, db_path=db)
    assert 'id' in res
    store = AttachmentStore(db)
    sha = store.get_sha_for_id(res['id'])
    assert sha is not None

