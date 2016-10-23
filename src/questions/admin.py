from django.contrib import admin
from models import *
# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
	list_display = ('question','relative_weight')

class OptionAdmin(admin.ModelAdmin):
	list_display = ('option', 'question', 'rank')

admin.site.register(Option, OptionAdmin)
admin.site.register(Question, QuestionAdmin)