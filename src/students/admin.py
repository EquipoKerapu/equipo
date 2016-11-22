from django.contrib import admin
from students.models import *
from django.db.models import Q

class SiteUserAdmin(admin.ModelAdmin):
    list_display = ('user',)

class StudentCourseMappingAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'rank',)

class ProfessorCourseMappingAdmin(admin.ModelAdmin):
    list_display = ('course', 'config')
    exclude = ('professor',)

    def get_queryset(self, request):
        qs = super(ProfessorCourseMappingAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs 
        return qs.filter(professor__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course":
            courses = ProfessorCourseMapping.objects.filter(professor__user=request.user).values_list('id', flat=True)
            kwargs["queryset"] = Course.objects.filter(Q(id__in=courses)| Q(created_by=request.user))
        elif db_field.name == "config":
            kwargs["queryset"] = Config.objects.filter(created_by=request.user)
        return super(ProfessorCourseMappingAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.professor = SiteUser.objects.get(user=request.user)
            obj.save()

admin.site.register(SiteUser, SiteUserAdmin)
admin.site.register(StudentCourseMapping, StudentCourseMappingAdmin)
admin.site.register(ProfessorCourseMapping, ProfessorCourseMappingAdmin)