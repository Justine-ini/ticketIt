from django.contrib import admin
from . models import Ticket, Sector, Company

# Register your models here.
admin.site.register(Ticket)
admin.site.register(Sector)
admin.site.register(Company)