from __future__ import annotations


import argparse 
import shutil
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path


CATEGORIES = {
    "Images": {".jpg" , ".jpeg" , ".png" , ".webp" , ".bmp"},
    "PDFs" : {".pdf"},
    "Documents" : {".doc" , ".docx" , ".txt" , ".md" , ".rtf"},
    "Spreadsheets" : {".xls" , ".xlsx" , ".csv" , ".tsv"},
    "PPTs" : {".ppt" , ".pptx"},
    "Archives" : {".rar" , ".zip" ,".7z" , ".tar" , ".gz"},
    "Installers" : {".exe" , ".msi"},
    "Code" : {".py" , ".js" , ".html" , ".css" , ".json" , ".xml" , ".cpp" , ".java"},
    "Audio" : {".mp3" , ".wav" , ".flac" , ".aac" , ".ogg"},
    "Videos" : {".mp4" , ".gif" , ".mov" , ".mkv" , ".avi" , ".webm"}
}
IGNORE_NAMES = {
    "desktop.ini",
    "thumbs.db",
}


@dataclass(frozen=True)
class MovePlan:
    source: Path
    destination: Path

def default_downloads_folder():
    return Path.home()/ "Downloads"


def category_in(file_path: Path):
    suffix = file_path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if suffix in extensions:
            return category
    return "Other"

def agecheck(file_path: Path, minimum_days: int):
    if minimum_days <= 0:
        return True
    mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
    return mod_time <= datetime.now() - timedelta(days= minimum_days)

def unique_des(des: Path):
    if not des.exists():
        return des
    counter = 1
    while True:
        candidate = des.with_name(
            f"{des.stem} ({counter}){des.suffix}"
        )
        if not candidate.exists():
            return candidate
        counter = counter + 1


def normalize_category_folder(downloads_folder: Path, category: str) -> Path:
    canonical = downloads_folder / category
    if canonical.exists():
        return canonical

    for item in downloads_folder.iterdir():
        if item.is_dir() and item.name.lower() == category.lower():
            temp = downloads_folder / f".{category}.tmp"
            item.rename(temp)
            temp.rename(canonical)
            return canonical

    return canonical


def BUILD_plan(downloads_folder:Path , minimum_days:int):
    plans: list[MovePlan] = []
    for item in downloads_folder.iterdir():
        if not item.is_file():
            continue
        if item.name.lower() in IGNORE_NAMES:
            continue
        if not agecheck(item,minimum_days):
            continue
        
        category = category_in(item)
        destination_folder = normalize_category_folder(downloads_folder, category)
        des = unique_des(destination_folder / item.name)
        plans.append(MovePlan(source=item , destination=des))
    return plans

def PRINT_plan(plans :list[MovePlan] , apply : bool):
    if not plans:
        print("Nothing to clean , your folder is already tidy lmao")
        return
    action = "Moving" if apply else "Would move"
    for plan in plans:
        file_name = plan.source.name
        destination = plan.destination.parent.name + "\\" + plan.destination.name
        print(action + ": " + file_name + " -> " + destination)
    
def APPLY_plan(plans : list[MovePlan]):
    for plan in plans:
        plan.destination.parent.mkdir(parents=True , exist_ok=True)
        shutil.move(str(plan.source) , str(plan.destination))

def parse_args():
    parser = argparse.ArgumentParser(
        description="Safely organize your downloads folder by file type"
    )
    parser.add_argument(
        "--folder",
        type=Path,
        default=default_downloads_folder(),
        help="Folder to clean . By default downloads folder"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually move files. Without this flag, the script only previews changes.",
    )
    parser.add_argument(
        "--min-age-days",
        type=int,
        default=0,
        help="Only move files at least this many days old. can be edited",
    )
    return parser.parse_args()

def main():
    args = parse_args()
    downloads_folder = args.folder.expanduser().resolve()
    
    if not downloads_folder.exists():
        raise SystemExit(f"Folder does not exist: {downloads_folder}")
    if not downloads_folder.is_dir():
        raise SystemExit(f"Not a folder: {downloads_folder}")
    if args.min_age_days < 0:
        raise SystemExit(f"--min-age-days cannot be NEGATIVE")
        
    plans = BUILD_plan(downloads_folder, args.min_age_days)
    PRINT_plan(plans , args.apply)

    if args.apply and plans:
        APPLY_plan(plans)
        print("Done.")
    elif plans:
        print("Preview only. Run again with --apply to move these files")

if __name__=="__main__":
    main()