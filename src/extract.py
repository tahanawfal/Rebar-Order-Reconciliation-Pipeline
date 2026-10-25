import json

import pandas as pd


class Extract:
    def __init__(self):
        pass

    def iterate_folder(self, source, folder_path):
        path_dict = {}
        for p in folder_path.rglob("*"):
            if p.is_file():
                path_dict[p.name] = folder_path
        return path_dict

    def read_excel(self, file_path) -> dict:
        return pd.read_excel(file_path, sheet_name=None, header=False)
    
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