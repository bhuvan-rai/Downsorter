import argparse 
import csv
import shutil
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import path


CATEGORIES = {
    "Images": {".jpg" , ".jpeg" , ".png" , ".webp" , ".bmp"},
    "PDFs" : {".pdf"},
    "Documents" : {".doc" , ".docx" , ".txt" , ".md" , ".rtf"},
    "Spreadsheets" : {".xls" , ".xlsx" , ".csv" , ".tsv"},
    "PPTs" : {".ppt" , ".pptx"},
    "archives" : {".rar" , ".zip" ,".7z" , ".tar" , ".gz"},
    "installers" : {".exe" , ".msi"},
    "Code" : {".py" , ".js" , ".html" , ".css" , ".json" , ".xml" , ".cpp" , ".java"},
    "Audio" : {".mp3" , ".wav" , ".flac" , ".aac" , ".ogg"},
    "Videos" : {".mp4" , ".gif" , ".mov" , ".mkv" , ".avi" , ".webm"}
}
