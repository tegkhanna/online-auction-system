from django.contrib import admin
from .models import *
from portal.models import *
# Register your models here.

class VisaInline(admin.TabularInline ):
    model = Visa
    extra=0
class ArticleInline(admin.TabularInline ):
    model = articlereg
    extra = 0
class Users(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['userName']}),
    ]
    inlines = [VisaInline, ArticleInline]
    list_display = ('userName', 'email', )

admin.site.register(UserDetail, Users)
admin.site.register(Admins)