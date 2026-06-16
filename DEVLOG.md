## Downsorter v0.1.0 Release

A lightweight CLI tool to organize messy folders by sorting files into category folders based on their extension.

**What it does:**
- Organizes files into folders by type (Images, Documents, PDFs, Code, Audio, Video, Archives, etc.)
- Safely previews changes before moving anything
- Handles file name collisions automatically
- Logs all moves for auditing
- Filters files by minimum age to avoid moving in-use files

**Install:**
```bash
pip install downsorter
```

**Quick start:**
```bash
# Preview what will happen
downsorter --folder "C:\Users\YourName\Downloads"

# Actually move the files
downsorter --folder "C:\Users\YourName\Downloads" --apply
```

**Key features:**
- ✅ Preview mode (safe by default)
- ✅ 11 file categories automatically sorted
- ✅ Duplicate file handling with auto-rename
- ✅ CSV move logging for auditing
- ✅ Cross-platform (Windows, macOS, Linux)
- ✅ No external dependencies

**Project links:**
- PyPI: https://pypi.org/project/downsorter/
- GitHub: https://github.com/yourusername/downsorter

Clean up your Downloads folder in seconds.
