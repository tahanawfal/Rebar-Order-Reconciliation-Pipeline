import json
import os

import pandas as pd


class Extract:
    def __init__(self):
        pass
    
    def csv_to_json(self, file_path):    
        df = pd.read_csv(file_path)
        data = df.set_index(df.columns[0]).to_dict(orient="index")
        
        file_folder_path = os.path.dirname(file_path)
        with open(rf"{file_folder_path}\columns_dict.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        with open(rf"{file_folder_path}\columns_dict.json", "r", encoding='utf-8') as file:
            data = json.load(file)
        return data