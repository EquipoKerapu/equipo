from django.contrib import admin
from students.models import Student
# Register your models here.

class StudentAdmin(admin.ModelAdmin):
	list_display = ('user',)

admin.site.register(Student, StudentAdmin)