import os
import csv
import pandas as pd
from .models import *
from django.conf import settings
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


# directory path to save export file
export_csv_dir = os.path.join(settings.BASE_DIR, 'media/export_csv')

# list of files of existing file
files = os.listdir(export_csv_dir)

# file name that will be visible as the download file name
file_name = 'csv_data.csv'
all_data_name = 'csv_data_all.csv'


@csrf_exempt
def csv_upload(request):
    if request.method == 'POST':
        # truncked all old data before upload new data
        StoreCode.objects.all().update(is_delete=True)
        try:
            if len(files) == 1:
                os.remove(os.path.join(export_csv_dir, files[0]))
        except:
            pass
        
        # File name that has uploaded from frontend 
        csv_file = request.FILES['csv_file']

        dataframe = None
        if str(csv_file).endswith(".xlsx"):
            dataframe = pd.read_excel(csv_file)
        if str(csv_file).endswith(".csv"):
            dataframe = pd.read_csv(csv_file)
        
        data = dataframe.values.tolist()
        
        # create the new data
        for row in data:
            StoreCode.objects.create(
                code = row[0],
                name = row[1],
                old_location = str(row[1]).split("_")[0] if str(row[1]).split("_")[0] else None,
                coming_stock = row[4],
                stock = row[5]
            )
        
        existing_data = StoreCode.objects.filter(is_delete=False)
        with open(os.path.join(export_csv_dir, file_name), mode='w', newline='') as export_file:
            writer = csv.writer(export_file)
            writer.writerow(['Code', 'Name', 'Old Location', 'New Location', 'Coming Stock', 'Stock'])

            # Write data rows
            for obj in existing_data:
                writer.writerow([obj.code, obj.name, obj.old_location, obj.new_location, obj.coming_stock, obj.stock])

        existing_data = StoreCode.objects.all()
        with open(os.path.join(export_csv_dir, all_data_name), mode='w', newline='') as export_file:
            writer = csv.writer(export_file)
            writer.writerow(['Code', 'Name', 'Old Location', 'New Location', 'Coming Stock', 'Stock'])

            # Write data rows
            for obj in existing_data:
                writer.writerow([obj.code, obj.name, obj.old_location, obj.new_location, obj.coming_stock, obj.stock])
    return redirect('/')


    
def get_code(request):
    if request.method == 'POST':
        request_code = request.POST['code']
        new_location = request.POST['new_location']
        try:
            if len(files) == 1:
                os.remove(os.path.join(export_csv_dir, files[0]))
        except:
            pass
        store_code_objects = StoreCode.objects.filter(code=request_code)
        if store_code_objects:
            StoreCode.objects.filter(code=request_code).update(code=request_code, new_location=new_location)
            messages.success(request, "Record Updated Successfully")
        else:
            StoreCode.objects.create(code=request_code, new_location=new_location)
            messages.success(request, "Record not available new record inserted")
          
        existing_data = StoreCode.objects.filter(is_delete=False)
        with open(os.path.join(export_csv_dir, file_name), mode='w', newline='') as export_file:
            writer = csv.writer(export_file)
            writer.writerow(['Code', 'Name', 'Old Location', 'New Location', 'Coming Stock', 'Stock'])

            # Write data rows
            for obj in existing_data:
                writer.writerow([obj.code, obj.name, obj.old_location, obj.new_location, obj.coming_stock, obj.stock])  

        existing_data = StoreCode.objects.all()
        with open(os.path.join(export_csv_dir, all_data_name), mode='w', newline='') as export_file:
            writer = csv.writer(export_file)
            writer.writerow(['Code', 'Name', 'Old Location', 'New Location', 'Coming Stock', 'Stock'])

            # Write data rows
            for obj in existing_data:
                writer.writerow([obj.code, obj.name, obj.old_location, obj.new_location, obj.coming_stock, obj.stock]) 
    return redirect('/')

def index(request): 
    return render(request, 'index.html')


class ExportCSVFile(APIView):
    def post(self, request):
        to_be_export = os.path.join(settings.BASE_DIR, 'media/export_csv')
        export_files = os.listdir(to_be_export)
        csv_file_path = None

        csv_file_path = {
                "csv_path" : f'/media/export_csv/{export_files[0]}'
                }
        return Response(csv_file_path)
    
class ExportAllCSVFile(APIView):
    def post(self, request):
        to_be_export = os.path.join(settings.BASE_DIR, 'media/export_csv')
        export_files = os.listdir(to_be_export)
        csv_file_path = None

        csv_file_path = {
                "csv_path" : f'/media/export_csv/{export_files[1]}'
                }
        return Response(csv_file_path)
    
class AllDelete(APIView):
    def delete(self, request):
        StoreCode.objects.all().delete()
        return Response({"massage":"all data deleted successfully"})
    
class ResponseOnCodeAPIView(APIView):
    def post(self, request):
        lookup_code = request.POST.get('lookup_code')
        if lookup_code:
            response = StoreCode.objects.filter(Q(code__iexact = lookup_code) | Q(code__icontains=lookup_code))
            if response.exists():
                return_response = [{"old_location" : objects.old_location, "new_location": objects.new_location,
                                    "old_stock" : objects.stock if objects.stock else 0, 
                                    "coming_stock" : objects.coming_stock if objects.coming_stock else 0} for objects in response]
                return Response(return_response)    
        return Response({"message" : "record not available"})