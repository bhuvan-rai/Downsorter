import argparse
import shutil
from json import load
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

@dataclass(frozen=True)
class MovePlan:
    source: Path
    destination: Path

class Sorter:
    def __init__(self, downloads_folder: Path, minimum_days: int):
        self.downloads_folder = downloads_folder
        self.minimum_days = minimum_days
        self.categories: dict[str, list[str]] = {}
        self.ignore_names: list[str] = []
        self.load_config(Path(__file__).parent / "base.config.json")

    def add_extensions(self, category: str, extensions: list[str]):
        if category in self.categories:
            for ext in extensions:
                if ext not in self.categories[category]:
                    self.categories[category].append(ext.lower())
        else:
            self.categories[category] = [ext.lower() for ext in extensions]

    def add_ignored_names(self, names: list[str]):
        for n in names:
            if n not in self.ignore_names:
                self.ignore_names.append(n.lower())

    def category_in(self, file_path: Path) -> str:
        suffix = file_path.suffix.lower()
        for category, extensions in self.categories.items():
            if suffix in extensions:
                return category
        return "Other"

    def load_config(self, config_path: Path):
        with open(config_path, "r") as f:
            config: dict[str, list[str]] = load(f)

        if config.get("categories"):
            for category, extensions in config["categories"].items():
                self.add_extensions(category, extensions)

        if config.get("ignore_names"):
            self.add_ignored_names(config.get("ignore_names"))

    def unique_des(self, des: Path) -> Path:
        if not des.exists():
            return des
        counter = 1
        while True:
            candidate = des.with_name(f"{des.stem} ({counter}){des.suffix}")
            if not candidate.exists():
                return candidate
            counter += 1

    def age_check(self, item: Path) -> bool:
        if self.minimum_days <= 0:
            return True
        mod_time = datetime.fromtimestamp(item.stat().st_mtime)
        return mod_time <= datetime.now() - timedelta(days= self.minimum_days)

    def normalize_category_folder(self, category: str) -> Path:
        canonical = self.downloads_folder / category
        if canonical.exists():
            return canonical
    
        for item in self.downloads_folder.iterdir():
            if item.is_dir() and item.name.lower() == category.lower():
                temp = self.downloads_folder / f".{category}.tmp"
                item.rename(temp)
                temp.rename(canonical)
                return canonical
        
        return canonical

    def build_plan(self) -> list[MovePlan]:
        plans: list[MovePlan] = []
        for item in self.downloads_folder.iterdir():
            if not item.is_file():
                continue
            if item.name.lower() in self.ignore_names:
                continue
            if not self.age_check(item):
                continue

            category = self.category_in(item)
            destination_folder = self.normalize_category_folder(category)
            des = self.unique_des(destination_folder / item.name)
            plans.append(MovePlan(source=item , destination=des))
        return plans

    def print_plan(self, plans: list[MovePlan], apply: bool):
        if not plans:
            print("Nothing to clean , your folder is already tidy lmao")
            return
        action = "Moving" if apply else "Would move"
        for plan in plans:
            file_name = plan.source.name
            destination = str(plan.destination.relative_to(self.downloads_folder))
            print(action + ": " + file_name + " -> " + destination)

    def apply_plan(self, plans: list[MovePlan]):
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
        default=(Path.home() / "Downloads"),
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
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to a JSON config file with custom categories and extensions.",
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

    planner = Sorter(downloads_folder, args.min_age_days)

    if args.config:
        if not args.config.exists():
            raise SystemExit(f"Config file does not exist: {args.config}")

        if not args.config.is_file():
            raise SystemExit(f"Not a file: {args.config}")

        planner.load_config(args.config)

    plans = planner.build_plan()
    planner.print_plan(plans, args.apply)

    if args.apply and plans:
        planner.apply_plan(plans)
        print("Done.")
    elif plans:
        print("Preview only. Run again with --apply to move these files")

if __name__=="__main__":
    main()