from django.urls import path
from .views import *


urlpatterns = [
    path("", index),
    path("csv_upload", csv_upload),
    path("get_code", get_code),
    path("api/export-csv", ExportCSVFile.as_view()),
    path("api/export-all-csv", ExportAllCSVFile.as_view()),
    path("api/all-delete", AllDelete.as_view()),
    path("api/lookup_code", ResponseOnCodeAPIView.as_view()),
]   