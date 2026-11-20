"""
Reset ALL designer test data so you can start again from DSN-0001.

Run this ONCE from your project folder (next to app.py) while the Flask app is STOPPED:

    python reset_designers.py

What it does
  * makes a backup copy of everything in  data/_backup_designers_<date-time>/
  * empties data/designers.xlsx            (headers are kept, all test designers removed)
  * empties data/designer_enquiries.xlsx   (test "Hire This Designer" enquiries removed)
  * empties data/designer_reviews.xlsx     (test ratings / reviews removed)
  * deletes data/designer_uploads/*        (uploaded portfolio / photo files)

It does NOT touch users, orders, bookings or inquiries.
"""
import os, shutil, sys
from datetime import datetime
from pathlib import Path
from openpyxl import load_workbook

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("DATA_DIR") or (BASE_DIR / "data")).resolve()
FILES = [DATA_DIR / "designers.xlsx", DATA_DIR / "designer_enquiries.xlsx", DATA_DIR / "designer_reviews.xlsx"]
UPLOADS = DATA_DIR / "designer_uploads"

print("Data folder:", DATA_DIR)
if input("This DELETES all designers + their uploads + enquiries + reviews (a backup is kept). Type YES to continue: ").strip() != "YES":
    sys.exit("Cancelled - nothing changed.")

backup = DATA_DIR / f"_backup_designers_{datetime.now():%Y%m%d_%H%M%S}"
backup.mkdir(parents=True)
for f in FILES:
    if f.exists():
        shutil.copy2(f, backup / f.name)
if UPLOADS.exists():
    shutil.copytree(UPLOADS, backup / "designer_uploads")
print("Backup saved in:", backup)

for f in FILES:
    if not f.exists():
        continue
    wb = load_workbook(f)
    ws = wb.active
    n = max(ws.max_row - 1, 0)
    if ws.max_row > 1:
        ws.delete_rows(2, ws.max_row - 1)
    wb.save(f)
    print(f"{f.name}: removed {n} row(s)")

if UPLOADS.exists():
    for child in UPLOADS.iterdir():
        shutil.rmtree(child, ignore_errors=True) if child.is_dir() else child.unlink(missing_ok=True)
    print("designer_uploads: cleared")

print("\nDone. Start the app again - the next designer will get DSN-0001.")