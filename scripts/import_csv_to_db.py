#!/usr/bin/env python3
"""Import CSV rows into the database using SQLModel async session.

Usage:
  python scripts/import_csv_to_db.py path/to/historical_figures_modern_era.csv

This script expects the CSV to have a header with column names that match the
Figure model fields (or a subset). Example header columns supported:
  name,birth_year,death_year,introduction,biography,contributions,image_intro,
  image_activity,image_ext_1,image_ext_2,video_1,video_2

The script inserts rows in batches and commits them asynchronously.
"""
import sys
import os
import csv
import asyncio
from typing import Dict, Any, List, Optional

# Ensure src is on path so we can import project modules without editing src
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
SRC_PATH = os.path.join(PROJECT_ROOT, 'src')
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from api.models.figure import Figure
from api.config.db_async import AsyncSessionLocal
from sqlmodel import select

# Fields on the Figure model that we will accept from CSV
ALLOWED_FIELDS = {
    'id', 'name', 'birth_year', 'death_year', 'introduction', 'biography', 'contributions',
    'image_intro', 'image_activity', 'image_ext_1', 'image_ext_2', 'video_1', 'video_2',
}

BATCH_SIZE = 100


def coerce_row(row: Dict[str, str]) -> Dict[str, Any]:
    """Convert CSV row strings into the types expected by the model."""
    out: Dict[str, Any] = {}
    for k, v in row.items():
        if k not in ALLOWED_FIELDS:
            continue
        if v is None:
            continue
        s = v.strip()
        if s == "":
            out[k] = None
            continue
        if k in ('birth_year', 'death_year', 'id'):
            try:
                out[k] = int(s)
            except ValueError:
                out[k] = None
        else:
            # limit lengths for URL/string fields if empty
            out[k] = s
    return out


async def insert_batch(records: List[Dict[str, Any]]):
    """Insert or update a batch of records.

    If a record includes an `id` that exists in the DB, update that row.
    Otherwise create a new row (allowing DB to assign an id when not provided).
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # find existing objects by id
            ids = [r['id'] for r in records if 'id' in r and r['id'] is not None]
            existing_map = {}
            if ids:
                stmt = select(Figure).where(Figure.id.in_(ids))
                result = await session.execute(stmt)
                for obj in result.scalars().all():
                    existing_map[obj.id] = obj

            for r in records:
                rid = r.get('id')
                if rid is not None and rid in existing_map:
                    obj = existing_map[rid]
                    for k, v in r.items():
                        if k == 'id':
                            continue
                        setattr(obj, k, v)
                    session.add(obj)
                else:
                    obj = Figure(**r)
                    session.add(obj)


async def import_csv(path: str):
    if not os.path.exists(path):
        raise SystemExit(f"CSV file not found: {path}")

    inserted = 0
    batch: List[Dict[str, Any]] = []

    with open(path, newline='') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            r = coerce_row(row)
            if not r.get('name'):
                # skip rows without a name
                continue
            batch.append(r)
            if len(batch) >= BATCH_SIZE:
                await insert_batch(batch)
                inserted += len(batch)
                print(f"Inserted {inserted} rows...")
                batch = []

    if batch:
        await insert_batch(batch)
        inserted += len(batch)
        print(f"Inserted {inserted} rows (final)")
    else:
        print(f"Inserted {inserted} rows")


def main(argv: Optional[List[str]] = None):
    argv = argv or sys.argv[1:]
    if not argv:
        print("Usage: import_csv_to_db.py path/to/file.csv")
        raise SystemExit(2)
    csv_path = argv[0]
    asyncio.run(import_csv(csv_path))


if __name__ == '__main__':
    main()
