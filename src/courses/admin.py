from django.contrib import admin
from models import *
# Register your models here.
class CourseAdmin(admin.ModelAdmin):
	list_display = ('course_title', )

admin.site.register(Course, CourseAdmin)