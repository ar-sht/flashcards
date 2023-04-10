import os
from pathlib import Path


class CSVModel:
    def __init__(self, filename=''):
        self.filename = filename

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

        terms = data['Terms']
        definitions = data['Definitions']

        with open(file, 'w', encoding='utf-8') as fh:
            for i in range(len(terms)):
                fh.write(f'{terms[i]},{definitions[i]}\n')

    def load_set(self):
        file = Path(self.filename)

        if not os.access(file, os.F_OK):
            raise PermissionError(f'Could not find set: {self.filename}')

        with open(file, 'r', encoding='utf-8') as fh:
            terms = []
            definitions = []
            for line in fh.readlines():
                line_data = line.split(',')
                terms.append(line_data[0].strip())
                definitions.append(line_data[1].strip())
        return zip(terms, definitions)
