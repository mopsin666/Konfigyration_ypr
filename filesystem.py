import zipfile
import os

class VFS:
    def __init__(self, zip_file):
        self.zip_file = zip_file
        self.zip = zipfile.ZipFile(zip_file, 'r')
        self.current_directory = "/"

    def list_files(self, path):
        # Вытаскиваем список файлов и директорий в заданном пути внутри архива.
        file_list = []
        for file in self.zip.namelist():
            if file.startswith(path):
                file_list.append(file)
        return file_list

    def extract_file(self, file_name, destination):
        with self.zip.open(file_name) as file:
            with open(destination, 'wb') as out_file:
                out_file.write(file.read())

    def extract_all(self, destination):
        for file in self.zip.namelist():
            self.extract_file(file, os.path.join(destination, file))

    def close(self):
        self.zip.close()
