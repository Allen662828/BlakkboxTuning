#!/usr/bin/env python3
"""CLI for ingesting unsorted files into the attachments DB."""
import argparse
from backend.unsorted_data.ingest import ingest_folder, ingest_file


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest='cmd')
    pi = sub.add_parser('ingest')
    pi.add_argument('--dir', required=False, help='Directory to ingest')
    pi.add_argument('--file', required=False, help='Single file to ingest')
    pi.add_argument('--link-bin', required=False, help='BIN SHA256 to link attachments to')
    pi.add_argument('--ocr', action='store_true')
    pi.add_argument('--db', default='data/attachments.db')

    ps = sub.add_parser('search')
    ps.add_argument('--query', required=True)
    ps.add_argument('--db', default='data/attachments.db')

    args = p.parse_args()
    if args.cmd == 'ingest':
        if args.file:
            r = ingest_file(args.file, link_to_bin=args.link_bin, ocr=args.ocr, db_path=args.db)
            print(r)
        elif args.dir:
            r = ingest_folder(args.dir, ocr=args.ocr, db_path=args.db)
            print('ingested', len(r), 'files')
        else:
            print('Provide --dir or --file')
    elif args.cmd == 'search':
        from backend.unsorted_data.storage import AttachmentStore
        s = AttachmentStore(args.db)
        res = s.search_text(args.query)
        for row in res:
            print(row)
    else:
        p.print_help()

if __name__ == '__main__':
    main()
