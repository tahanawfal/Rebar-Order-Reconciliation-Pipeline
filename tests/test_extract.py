import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.extract import Extract
from src.manage_dates import ManageDates

extract = Extract()
manage_dates = ManageDates()

# paths of input and output data folders
input_path = Path("./data/input")
output_path = Path("./data/output")

# paths of sources of input data folders
input_folders = {
    "sales": input_path / "sales",
    "dispatch": input_path / "dispatch",
    "weighbridge": input_path / "weighbridge",
}

# creating lists of file pathes inside these input folders
# files = extract.iterate_folder(input_folders)

excel_path = Path('data/input/sales/2026-08/26-8.xlsx')
source = 'sales'

sheet_dict = extract.read_excel('data/input/sales/2026-08/26-8.xlsx')
# print(sheet_dict['حديد تسليح'])

p = manage_dates.export_dates_from_file(excel_path)
print(p)