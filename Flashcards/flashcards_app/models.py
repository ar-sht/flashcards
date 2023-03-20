import os
import csv
from pathlib import Path


def save_set(data, filename='misc_cards.csv'):
    file = Path(filename)

    file_exists = os.access(file, os.F_OK)
    parent_writeable = os.access(file.parent, os.W_OK)
    file_writeable = os.access(file, os.W_OK)

    if (
            (not file_exists and not parent_writeable) or
            (file_exists and not file_writeable)
    ):
        msg = f'Permission denied accessing file: {filename}'
        raise PermissionError(msg)

    newfile = not file.exists()
    with open(file, 'a', newline='') as fh:
        csvwriter = csv.DictWriter(fh, fieldnames=['Prompts', 'Responses'])
        if newfile:
            csvwriter.writeheader()
        csvwriter.writerow(data)


def load_set(filename):
    file = Path(filename)

    if not os.access(file, os.F_OK):
        raise PermissionError(f'Could not find set: {filename}')

    with open(file, 'r') as fh:
        csvreader = csv.DictReader(fh, fieldnames=['Prompts', 'Responses'])
        return dict(csvreader)
