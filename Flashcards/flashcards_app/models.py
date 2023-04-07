import os
import csv
from pathlib import Path


class CSVModel:
    def __init__(self, filename='Untitled'):
        self.filename = filename + '.csv'

    def save_set(self, data):
        file = Path(self.filename)
        file_exists = os.access(file, os.F_OK)
        parent_writeable = os.access(file.parent, os.W_OK)
        file_writeable = os.access(file, os.W_OK)

        if (
                (not file_exists and not parent_writeable) or
                (file_exists and not file_writeable)
        ):
            msg = f'Permission denied accessing file: {self.filename}'
            raise PermissionError(msg)

        i = 0
        if self.filename == 'Untitled':
            while file_exists:
                self.filename = self.filename[:-4] + f' ({i})' + self.filename[-4:]
                file = Path(self.filename)
                i += 1

        newfile = not file.exists()
        with open(file, 'a', newline='') as fh:
            csvwriter = csv.DictWriter(fh, fieldnames=['Terms', 'Definitions'])
            if newfile:
                csvwriter.writeheader()
            csvwriter.writerow(data)

    def load_set(self):
        file = Path(self.filename)

        if not os.access(file, os.F_OK):
            raise PermissionError(f'Could not find set: {self.filename}')

        with open(file, 'r') as fh:
            csvreader = csv.DictReader(fh, fieldnames=['Prompts', 'Responses'])
            return dict(csvreader)
