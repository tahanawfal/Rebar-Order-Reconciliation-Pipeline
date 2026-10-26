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
        self.get_creation_date()
        self.get_modification_date()
        self.get_date_from_folder_name()
        self.get_date_from_file_name()
    
    def export_dates_from_file(self, file_path):
        return {
            'file_path': file_path.as_posix(),
            'file_creation_date': self.get_creation_date(),
            'file_modification_date': self.get_modification_date(),
            'folder_name_date': self.get_date_from_folder_name(),
            'file_name_date': self.get_date_from_file_name()
        }

    def get_creation_date(self, file_path):
        timestamp = Path(file_path).stat().st_ctime
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

    def get_modification_date(self, file_path):
        timestamp = Path(file_path).stat().st_mtime
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    
    def get_date_from_folder_name(self, file_path):
        folder_name = file_path.parent.absolute().name.strip()
        for format in self.commmon_formats:
            try:
                dt = datetime.strptime(folder_name, format)
                return dt.strftime("%Y-%m")
            except ValueError:
                continue
      
    def get_date_from_file_name(self, file_path):
        file_name = file_path.stem.strip()
        for format in self.commmon_formats:
            try:
                dt = datetime.strptime(file_name, format)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue



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