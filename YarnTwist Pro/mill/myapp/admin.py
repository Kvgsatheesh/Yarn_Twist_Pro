from django.contrib import admin
from .models import Company,Colour,Stocks

# Register your models here


admin.site.register(Company)
admin.site.register(Colour)
admin.site.register(Stocks)
