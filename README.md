# Downsorter

A small Python CLI tool that organizes files by extension into category folders.

Use it to clean up a messy folder, especially downloads, by moving images, documents, archives, installers, code, audio, and video files into the right subfolders.

## Features

- Organizes files by extension into category folders
- Preview mode so you can see changes before moving anything
- Safe move mode with `--apply` to actually perform the file moves
- Handles duplicate names by renaming files to `name (1).ext`, `name (2).ext`, etc.
- Ignores common system files like `desktop.ini` and `thumbs.db`
- Supports minimum file age filtering with `--min-age-days`
- Works on Windows, macOS, and Linux with Python 3.10+

## Platform Support

| Platform | Support | Notes |
| --- | --- | --- |
| Windows 10/11 | Supported | Best tested platform for this project |
| macOS | Supported | Works with Python 3.10+ |
| Linux | Supported | Works with Python 3.10+ |

## Files

- `sorter.py` - main CLI script and package entry point
- `README.md` - project instructions
- `pyproject.toml` - package metadata for PyPI
- `LICENSE` - MIT license text

## Install

### From PyPI ( run this in powershell)

```bash
pip install downsorter
```

## Usage

### Preview what will happen

This is the safest way to run the tool first.

```bash
downsorter --folder "C:\Users\YourName\Downloads"(or put path inside "" of whatever folder you want to sort)
```

### Actually move files

```bash
downsorter --folder "C:\Users\YourName\Downloads"(or put path inside "" of whatever folder you want to sort) --apply
```

### EG: Only move files older than 7 days ( default days is 0 , i.e no requirement)

```bash
downsorter --folder "C:\Users\YourName\Downloads" --min-age-days 7 --apply
```

## Options

- `--folder`: Folder to organize. Defaults to the current user's Downloads folder.
- `--apply`: Actually move files. Without this flag, the script only previews the planned moves.
- `--min-age-days`: Only move files that have not been modified for at least this many days.

## How it works

1. The script scans the target folder for files.
2. It matches each file extension against a category list.
3. It builds a plan showing where each file would move.
4. In preview mode, it only prints the plan.
5. In apply mode, it creates category folders, moves files, and logs the results.

## Categories

The project currently sorts files into:

- `Images` (.jpg, .jpeg, .png, .webp, .bmp)
- `PDFs` (.pdf)
- `Documents` (.doc, .docx, .txt, .md, .rtf)
- `Spreadsheets` (.xls, .xlsx, .csv, .tsv)
- `PPTs` (.ppt, .pptx)
- `Archives` (.rar, .zip, .7z, .tar, .gz)
- `Installers` (.exe, .msi)
- `Code` (.py, .js, .html, .css, .json, .xml, .cpp, .java)
- `Audio` (.mp3, .wav, .flac, .aac, .ogg)
- `Videos` (.mp4, .gif, .mov, .mkv, .avi, .webm)
- `Other` for everything else

## Example

Run this to preview then apply:

```bash
downsorter --folder "C:\Users\YourName\Downloads"
downsorter --folder "C:\Users\YourName\Downloads" --apply
```

## License

This project is licensed under the MIT License.
