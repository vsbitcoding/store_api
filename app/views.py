import os
import csv
import pandas as pd
from .models import *
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from django.db import transaction

@csrf_exempt
@transaction.atomic
def csv_upload(request):

    if request.method == 'POST':
        # Truncate all old data before uploading new data
        StoreCode.objects.all().update(is_delete=True)

        # File name that has been uploaded from the frontend
        csv_file = request.FILES['csv_file']

        if str(csv_file).endswith(".xlsx"):
            # Read XLSX file
            dataframe = pd.read_excel(csv_file)
        elif str(csv_file).endswith(".csv"):
            # Read CSV file
            dataframe = pd.read_csv(csv_file)
        else:
            # Invalid file format
            return HttpResponse("Invalid file format", status=400)

        data = dataframe.to_dict('records')

        # Create the new data using bulk_create()
        objects_to_create = [
            StoreCode(
                code=row['Code'],
                name=row['Name'],
                old_location=str(row['Name']).split("_")[0] if str(row['Name']).split("_")[0] else None,
                new_location=row['New Location'],
                coming_stock=row['Coming Stock'],
                stock=row['Stock']
            )
            for row in data
        ]
        StoreCode.objects.bulk_create(objects_to_create)

    return redirect('/')

@csrf_exempt
def get_code(request):
    if request.method == 'POST':
        request_code = request.POST.get('code')
        new_location = request.POST.get('new_location')

        store_code = StoreCode.objects.filter(code=request_code, is_delete=False).first()

        if store_code:
            store_code.new_location = new_location
            store_code.save()
            messages.success(request, "Record Updated Successfully")
        else:
            StoreCode.objects.create(code=request_code, new_location=new_location)
            messages.success(request, "New Record Inserted")

    return redirect('/')

def index(request): 
    return render(request, 'index.html')

class ExportCSVFile(APIView):
    def post(self, request):
        data = StoreCode.objects.filter(is_delete=False)
        csv_file_path = os.path.join(settings.BASE_DIR, 'media/export_csv/data.csv')
        with open(csv_file_path, mode='w', newline='') as export_file:
            writer = csv.writer(export_file)
            writer.writerow(['Code', 'Name', 'Old Location', 'New Location', 'Coming Stock', 'Stock'])

            for obj in data:
                writer.writerow([obj.code, obj.name, obj.old_location, obj.new_location, obj.coming_stock, obj.stock])

        response_data = {
            "csv_path": f'/media/export_csv/data.csv'
        }
        return JsonResponse(response_data)

from django.http import JsonResponse

class ExportAllCSVFile(APIView):
    def post(self, request):
        data = StoreCode.objects.all()

        csv_file_path = os.path.join(settings.BASE_DIR, 'media/export_csv/all_data.csv')
        with open(csv_file_path, mode='w', newline='') as export_file:
            writer = csv.writer(export_file)
            writer.writerow(['Code', 'Name', 'Old Location', 'New Location', 'Coming Stock', 'Stock'])

            for obj in data:
                writer.writerow([obj.code, obj.name, obj.old_location, obj.new_location, obj.coming_stock, obj.stock])

        response_data = {
            "csv_path": f'/media/export_csv/all_data.csv'
        }
        return JsonResponse(response_data)

class AllDelete(APIView):
    def delete(self, request):
        StoreCode.objects.all().delete()
        return Response({"massage":"all data deleted successfully"})
    
class ResponseOnCodeAPIView(APIView):
    def post(self, request):
        lookup_code = request.POST.get('lookup_code')
        if lookup_code:
            response = StoreCode.objects.filter(code__iexact = lookup_code,is_delete=False)
            if response.exists():
                return_response = [{"old_location" : objects.old_location, "new_location": objects.new_location,
                                    "old_stock" : objects.stock if objects.stock else 0, 
                                    "coming_stock" : objects.coming_stock if objects.coming_stock else 0} for objects in response]
                return Response(return_response)    
        return Response({"message" : "record not available"})