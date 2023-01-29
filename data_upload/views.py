from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from data_upload.serializers import PersonSerializer


class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    permission_classes = (IsAuthenticated,)
    serializer_class = PersonSerializer

    @swagger_auto_schema(
        operation_description='Upload EXCEL file with headers name, email, phone_number',
        manual_parameters=[openapi.Parameter(
            name="file",
            in_=openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            required=True,
            description="File"
        )],
    )
    @action(detail=False, methods=['post'], parser_classes=(FormParser,))
    def post(self, request, *args, **kwargs):
        file_obj = request.data['file']
        file_serializer = self.serializer_class(data=request.data, context={"file_obj": file_obj})
        file_serializer.upload_file()

        return Response({"message": "Thank you! Your file upload is in progress."}, status=status.HTTP_200_OK)
