from django.contrib import admin
from students.models import *
# Register your models here.

class SiteUserAdmin(admin.ModelAdmin):
	list_display = ('user',)

class StudentCourseMappingAdmin(admin.ModelAdmin):
	list_display = ('student', 'course', 'rank',)

class ProfessorCourseMappingAdmin(admin.ModelAdmin):
	list_display = ('professor', 'course')

admin.site.register(SiteUser, SiteUserAdmin)
admin.site.register(StudentCourseMapping, StudentCourseMappingAdmin)
admin.site.register(ProfessorCourseMapping, ProfessorCourseMappingAdmin)