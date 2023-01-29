import os
import time

import pandas as pd
from pathlib import Path

from data_upload.models import Person
from hacktech.settings import BASE_DIR
from django.core.files import File

TEMPORARY_FILES_FOLDER_NAME = 'temporary_files'
TEMPORARY_FILE_NAME_DATE_FORMAT = '%Y-%m-%d-%H-%M-%S'


def create_temporary_file(prefix: str, data: list):
    """
    Create temporary .txt files for comparing
    """
    dir_path = Path(f"{BASE_DIR}/{TEMPORARY_FILES_FOLDER_NAME}")
    file_name = f"{prefix}_{time.strftime(TEMPORARY_FILE_NAME_DATE_FORMAT)}.txt"
    file_path = dir_path.joinpath(file_name)
    with open(file_path, 'w') as f:
        f.write(", ".join(data))


def prepare_records_to_insert(records_list: list, compared_data=None):
    """
    Prepare records which should inserted to database
    """
    persons_list, temporary_data = [], []
    for record in records_list:
        name, email, phone_number = record.get("name"), record.get("email"), record.get("phone_number")
        if not phone_number:
            continue

        if compared_data and (email in compared_data or phone_number in compared_data):
            continue

        temporary_data.append(str(phone_number))
        temporary_data.append(str(email)) if email else None
        persons_list.append(Person(name=name, email=email, phone_number=phone_number))
        create_temporary_file("temporary_data", temporary_data)

    return persons_list


def get_excel_file_headers(file) -> list:
    """
    Get excel headers
    """
    excel_records = pd.read_excel(file)
    return excel_records.columns.ravel()


def delete_temporary_files(temporary_files: list):
    """
    Delete temporary file if 3 minutes have passed since the file was created
    """
    current_time = time.time()
    for tmp_file in temporary_files:
        if (current_time - os.path.getctime(f"{BASE_DIR}/{TEMPORARY_FILES_FOLDER_NAME}/{tmp_file}")) / 60 >= 3:
            os.remove(f"{BASE_DIR}/{TEMPORARY_FILES_FOLDER_NAME}/{tmp_file}")


def get_temporary_files_data() -> list:
    """
    Get temporary file data
    """
    compared_data = []
    for temporary_file in os.listdir(f"{BASE_DIR}/{TEMPORARY_FILES_FOLDER_NAME}"):
        temporary_file_data = open(f"{BASE_DIR}/{TEMPORARY_FILES_FOLDER_NAME}/{temporary_file}", "r")
        data = temporary_file_data.read()
        data_into_list = [i.strip() for i in data.split(",")]
        compared_data += data_into_list

    return compared_data


def get_records_from_excel(file, file_obj) -> list:
    """
    Get records from excel
    """
    excel_file = File(file, name=file_obj.name)
    excel_records = pd.read_excel(excel_file)
    excel_records.fillna('', inplace=True)
    return excel_records.to_dict("records")
