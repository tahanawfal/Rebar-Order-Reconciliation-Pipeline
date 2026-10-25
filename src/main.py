from pathlib import Path

from clean_values import CleanValues
from cumulative import Cumulative
from extract import Extract
from manage_dates import ManageDates
from sheet_to_table import SheetToTable
from table_to_structured import TableToStructured

# Classes Inheritance 
extract = Extract()
manage_dates = ManageDates()
sheet_to_table = SheetToTable()
table_to_structured = TableToStructured()
clean_values = CleanValues()
cumulative = Cumulative()

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
for source_name, source_path in input_folders.items():
    files = extract.iterate_folder(source_name , source_path)

for excel_path, source in files.items():
    # get file properties before reading it
    excel_dates = manage_dates.export_dates_from_file(excel_path)
    # read all sheets inside the excel file and save it into dict var
    sheet_dict = extract.read_excel(excel_path)
    # choose the target sheets with a correct name
    sheet_dict = extract.filter_sheet(sheet_dict)

    for sheet_name, sheet in sheet_dict.items():
        if source == "sales":
            first_row_date = manage_dates.export_date_from_first_row(sheet)

        if source == "sales" or source == "dispatch":
            sheet = sheet_to_table.remove_top_empty_rows(sheet, "CUSTOMER")
            header = sheet_to_table.merge_the_header(sheet)
        df = sheet_to_table.set_header(sheet, header)
        df = sheet_to_table.unify_columns(df)
        df = sheet_to_table.remove_footers(df)
        
        df = table_to_structured.remove_empty(df)
        if source == "sales":
            df = table_to_structured.fill_nulls(df)
            df = table_to_structured.set_date_column(df, first_row_date)
        else:
            df = clean_values.format_dates(df)
        min_date, max_date = manage_dates.get_min_max_dates(df)
        df = manage_dates.set_file_dates_column(df, excel_dates, min_date, max_date)
        df = manage_dates.set_identifer_date(df)
        manage_dates.append_into_sheets_report(df)
        
    cumulative.report_missing_files()

