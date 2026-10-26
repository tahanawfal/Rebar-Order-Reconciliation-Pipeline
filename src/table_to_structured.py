import pandas as pd


class TableToStructured:
    def __init__(self):
        pass

    def remove_empty(self):
        pass

    def fill_nulls(self):
        pass

    def set_date_column(self, df, date):
        df[len(df.columns)] = date
        df.iloc[0, -1] = "log_date"