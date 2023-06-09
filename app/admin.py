from django.contrib import admin
from .models import StoreCode

class StoreCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'old_location', 'new_location', 'coming_stock', 'stock', 'is_delete']
    list_filter = ['is_delete']

admin.site.register(StoreCode, StoreCodeAdmin)

