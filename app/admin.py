from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib import admin
from .models import StoreCode

class YourModelAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

admin.site.register(StoreCode, YourModelAdmin)
