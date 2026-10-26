import json
from pathlib import Path

import pandas as pd


class Extract:
    def __init__(self):
        pass

    def iterate_folder(self, folder_path: dict[str, Path]) -> dict[Path, str]:
        path_dict = {}
        for source_name, source_path in folder_path.items():
            for path in source_path.rglob("*"):
                if path.is_file():
                    path_dict[path.as_posix()] = source_name
        return path_dict

    def read_excel(self, file_path) -> dict:
        return pd.read_excel(file_path, sheet_name=None, header=None)
    
    def filter_sheet(self):
        pass

    def csv_to_json(self, file_path):    
        # read the csv file
        df = pd.read_csv(file_path)
        data = df.set_index(df.columns[0]).to_dict(orient="index")
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        with open(file_path, "r", encoding='utf-8') as file:
            data = json.load(file)
        return data