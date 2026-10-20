from pathlib import Path

from extract import Extract
from normalize import Normalize
from scan import Scan

input_path = Path("./data/input")
sales_path = input_path / "sales"
dispatch_path =  input_path / "dispatch"
weighbridge_path = input_path / "weighbridge"
test_file = dispatch_path + "2024-01" / "21jan24.xlsx"

extract = Extract()
normalize = Normalize()
scan = Scan()

extract.csv_to_json(input_path / "lookup", "columns_dict.json")

# data = extract.read_excel(
#     file_path=r".\data\input\dispatch\excel\2026-10",
#     file_name="15-10-2026.xlsx",
#     sheet_name="DAILY SALES",)

print(extract.get_date_from_file_name())

# table = normalize.remove_top_empty_rows(file=data, column_name="CUSTOMER")

# # 1. Assign combined headers to table columns
# table.columns = new_columns

# # 2. Slice off rows 0 and 1 so they don't remain as data rows
# table = table.iloc[2:].copy()

# # 3. Drop rows where CUSTOMER is missing
# table = table.dropna(subset=["CUSTOMER"])
# table = table[table["CUSTOMER"].astype(str).str.strip().ne("")]

# # 4. Reset index
# table.reset_index(drop=True, inplace=True)

# print(table.info())

