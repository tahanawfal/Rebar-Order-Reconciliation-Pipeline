from pathlib import Path


class Scan:
    def __init__(self):
        pass

    def iterate_folder(self, folder_path, applied_function, *args, **kwargs):
        root = Path(folder_path)
        
        for item in root.rglob('*'):
            if item.is_file():
                applied_function(item, *args, **kwargs)