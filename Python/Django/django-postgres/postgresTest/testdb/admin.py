from django.contrib import admin
from testdb.models import Teacher
# Register your models here.

@admin.register(Teacher)
class AuthorAdmin(admin.ModelAdmin):
    pass