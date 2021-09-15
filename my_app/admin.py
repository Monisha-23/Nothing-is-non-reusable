from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
admin.site.register(home)
admin.site.register(shopkeeper)
admin.site.register(garbagecollecter)
admin.site.register(company)
admin.site.register(volunteer)
admin.site.register(contact)
admin.site.register(vacancy)
admin.site.register(shopvol)
admin.site.register(garvol)
admin.site.register(comvol)
admin.site.register(Requests)
admin.site.register(Requests_S)
admin.site.register(Requests_G)
admin.site.register(apply)
admin.site.register(Quote)