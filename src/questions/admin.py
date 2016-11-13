from django.contrib import admin
from models import *
# Register your models here.
class OptionInline(admin.TabularInline):
	model = Option

class QuestionAdmin(admin.ModelAdmin):
	list_display = ('question_text','relative_weight')
	inlines = [OptionInline]


class ConfigAdmin(admin.ModelAdmin):
	list_display = ('name',)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Config, ConfigAdmin)