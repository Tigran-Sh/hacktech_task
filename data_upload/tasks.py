import os
from pathlib import Path

from celery import shared_task

from data_upload.models import Person
from data_upload.utils import prepare_records_to_insert, delete_temporary_files, \
    get_temporary_files_data, get_records_from_excel
from hacktech.settings import BASE_DIR
from services.storage_management import StorageManagement

TEMPORARY_FILES_FOLDER_NAME = 'temporary_files'


@shared_task
def upload(path: str):
    """
    Upload file contacts data to database

    The same email address/phone number cannot be uploaded in a time
    window of 3 minutes. After 3 minutes have passed, contact with that email/phone number can be uploaded.

    The email/phone number time window case is solved by adding temporary files.
    In case if temporary files exists, it checks:
        1. if 3 minutes have passed since the file was created then I just delete this file
        2. if not, I make list from txt file content and merge with other files if exists
        3. I make a validation, if email/phone number exists in merged list I didn't add records to inserted list

    :param: path of the upload file
    """
    file_obj = StorageManagement.get_file(path)

    if not Path("temporary_files").is_dir():
        os.makedirs("temporary_files")

    with file_obj.open(mode='rb') as file:
        records_list = get_records_from_excel(file, file_obj)
        temporary_files = os.listdir(f"{BASE_DIR}/{TEMPORARY_FILES_FOLDER_NAME}")
        if temporary_files:
            delete_temporary_files(temporary_files)
            compared_data = get_temporary_files_data()
            persons_list = prepare_records_to_insert(records_list, compared_data)
        else:
            # In case if temporary files directory is empty then add records to model where phone number not none
            persons_list = prepare_records_to_insert(records_list)

        Person.objects.bulk_create(persons_list)
