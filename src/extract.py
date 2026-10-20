import json
from datetime import datetime
from pathlib import Path

import pandas as pd


class Extract:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.file_name = self.file_path.stem

    def read_excel(self, sheet_name: str, header=True):
        return pd.read_excel(self.file_path, sheet_name=sheet_name, header=header)
    
    def csv_to_json(self):    
        # read the csv file
        df = pd.read_csv(self.file_path)
        data = df.set_index(df.columns[0]).to_dict(orient="index")
        
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        with open(self.file_path, "r", encoding='utf-8') as file:
            data = json.load(file)
        return data


    def get_creation_date(self):
        file_stat = self.file_path.stat()
        
        # macOS and FreeBSD support st_birthtime directly
        if hasattr(file_stat, 'st_birthtime'):
            timestamp = file_stat.st_birthtime
        else:
            # On Windows, st_ctime is the file creation time.
            # On Linux, st_ctime is the last metadata change time (chmod, rename, etc.),
            # so st_mtime (last modified) is often the closest reliable proxy.
            import platform
            if platform.system() == "Windows":
                timestamp = file_stat.st_ctime
            else:
                timestamp = file_stat.st_mtime

        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

    def get_date_from_file_name(self):
        # return self.file_name.strftime('%Y-%m-%d')
        COMMON_FORMATS = [
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%d%b%Y",
            "%Y%b%d",
            "%y-%m-%d",
            "%d-%m-%y",
            "%d%b%y",
            "%y%b%d",
            "%d-%m"
        ]

        for fmt in COMMON_FORMATS:
            try:
                return datetime.strptime(self.file_name, fmt).date()
            except ValueError:
                continue
        raise ValueError(f"Could not parse '{self.file_name}' with known formats.")