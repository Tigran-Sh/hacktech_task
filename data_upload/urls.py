from django.urls import path
from .views import *

urlpatterns = [
    path('upload-excel/', FileView.as_view(), name="upload-excel"),
]
