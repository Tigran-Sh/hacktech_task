from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from services.storage_management import StorageManagement
from .tasks import upload
from data_upload.models import Person
from .utils import get_excel_file_headers


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

    def upload_file(self):
        file = self.context["file_obj"]
        self.validate_headers(file)
        storage_obj = StorageManagement()
        storage_obj.save_file(file)

        return upload.delay(path=storage_obj.get_storage_path())

    @classmethod
    def validate_headers(cls, file):
        headers = get_excel_file_headers(file)
        required_fields = ["name", "email", "phone_number"]
        for header in headers:
            header = header.lower().replace(" ", "_")
            if header not in required_fields:
                raise ValidationError({"error_message": f"Headers should have the following headers {required_fields}"})
