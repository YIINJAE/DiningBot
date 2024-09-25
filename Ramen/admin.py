from django.contrib import admin
from .models import MyModel

class MyModelAdmin(admin.ModelAdmin):
    search_fields = ['date']

admin.site.register(MyModel, MyModelAdmin)