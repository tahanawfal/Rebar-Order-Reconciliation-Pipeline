import pandas as pd


class Normalize:
    def __init__(self):
        pass

    def remove_top_empty_rows(self, file, column_name: str):
        empty_top_rows = file[file.isin([column_name]).any(axis=1)].index[0]
        file = file.iloc[empty_top_rows:].copy()
        return file

    def merge_double_header(self, file):
        header_row_1 = file.iloc[0]
        header_row_2 = file.iloc[1]
        self.new_columns = [str(bottom) if pd.notna(bottom) else str(top) for top, bottom in zip(header_row_1, header_row_2)]