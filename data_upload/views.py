from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from data_upload.serializers import PersonSerializer


class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    permission_classes = (IsAuthenticated,)
    serializer_class = PersonSerializer

    def post(self, request, *args, **kwargs):
        file_obj = request.data['file']
        file_serializer = self.serializer_class(data=request.data, context={"file_obj": file_obj})
        file_serializer.upload_file()

        return Response({"message": "Thank you! Your file upload is in progress."}, status=status.HTTP_200_OK)
