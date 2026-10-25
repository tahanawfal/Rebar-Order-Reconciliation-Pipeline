from datetime import datetime
from pathlib import Path


class ManageDates:
    def __init__(self):
        self.commmon_formats = [
            "%#d-%#m-%Y",
            "%d-%m-%Y",
            "%#d%b%y",
            "%d%b%y",
            "%Y-%m",
            "%#d-%#m",
            "%d-%m",
            "%Y"
        ]
    
    def get_creation_date(self, file_path):
        file_stat = Path(file_path).stat()
        timestamp = file_stat.st_mtime
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    
    def get_date_from_folder_name(self, file_path):
        folder_name = Path(file_path).parent.absolute()
        for format in self.commmon_formats:
            try:
                dt = datetime.strptime(folder_name.name.strip(), format)
                return dt
            except ValueError:
                continue
      
    def get_date_from_file_name(self, file_path):
        file_name = Path(file_path).stem
        for format in self.commmon_formats:
            try:
                dt = datetime.strptime(file_name.strip(), format)
                return dt
            except ValueError:
                continue

    def export_dates_from_file(self):
        pass

    def export_date_from_first_row(self):
        pass
    
    def get_min_max_dates(self, file_path):
        pass

    def set_file_dates_column(self):
        pass

    def set_identifer_date(self):
        pass

    def append_into_sheets_report(self):
        pass