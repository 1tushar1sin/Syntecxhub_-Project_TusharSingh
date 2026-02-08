import os
import shutil
import logging
import argparse
from datetime import datetime

def setup_logger(logfile):
    logging.basicConfig(
        filename=logfile,
        level=logging.INFO,
        format='%(asctime)s - %(message)s'
    )

def get_unique_filename(dest_folder, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(dest_folder, new_filename)):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1
    return new_filename

def move_files_by_extension(folder, dry_run=False, logfile='file_move.log'):
    setup_logger(logfile)
    for fname in os.listdir(folder):
        fpath = os.path.join(folder, fname)
        if os.path.isfile(fpath):
            ext = os.path.splitext(fname)[1][1:] or 'no_ext'
            dest_folder = os.path.join(folder, ext)
            if not os.path.exists(dest_folder):
                if not dry_run:
                    os.makedirs(dest_folder)
            unique_name = get_unique_filename(dest_folder, fname)
            dest_path = os.path.join(dest_folder, unique_name)
            if dry_run:
                print(f"[DRY RUN] Would move: {fpath} -> {dest_path}")
            else:
                shutil.move(fpath, dest_path)
                logging.info(f"Moved: {fpath} -> {dest_path}")
                print(f"Moved: {fpath} -> {dest_path}")

def main():
    parser = argparse.ArgumentParser(description='Move files into subfolders by extension.')
    parser.add_argument('folder', help='Folder to scan')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be moved without making changes')
    parser.add_argument('--logfile', default='file_move.log', help='Log file for moved files')
    args = parser.parse_args()
    move_files_by_extension(args.folder, dry_run=args.dry_run, logfile=args.logfile)
    print("Done.")
    print("To schedule, use Windows Task Scheduler or cron.")
    print("Example: python script.py C:/Users/YourName/Desktop --dry-run")

if __name__ == "__main__":
    main()
