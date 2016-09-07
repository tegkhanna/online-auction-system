from django.contrib import admin
from .models import *
# Register your models here.

class VisaInline(admin.TabularInline ):
    model = Visa
class Users(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['userName']}),
    ]
    inlines = [VisaInline]
    list_display = ('userName', 'email', )

admin.site.register(UserDetail, Users)