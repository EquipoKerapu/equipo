from django.contrib import admin
from models import *
# Register your models here.


class OptionInline(admin.TabularInline):
    model = Option
    exclude = ('created_by', 'created_on')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text','relative_weight')
    exclude = ('created_by', 'created_on')
    inlines = [OptionInline]

    def get_queryset(self, request):
        qs = super(QuestionAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs 
        return qs.filter(created_by=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.save()

    def save_formset(self, request, form, formset, change):
        formset.save()
        if not change:
            for f in formset.forms:
                obj = f.instance 
                obj.created_by = request.user
                obj.save()


class ConfigAdmin(admin.ModelAdmin):
    list_display = ('name',)
    exclude = ('created_by', 'created_on')

    def get_queryset(self, request):
        qs = super(ConfigAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs 
        return qs.filter(created_by=request.user)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "questions":
            kwargs["queryset"] = Question.objects.filter(created_by=request.user)
        return super(ConfigAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.save()


admin.site.register(Question, QuestionAdmin)
admin.site.register(Config, ConfigAdmin)