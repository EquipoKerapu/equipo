from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Question(models.Model):
	question_text = models.CharField(max_length=255)
	relative_weight = models.IntegerField(choices=[(i,i) for i in range(1,11)])

	def __unicode__(self):
		return self.question_text

class Option(models.Model):
	question = models.ForeignKey(Question, related_name='question_options')
	option = models.CharField(max_length=255)
	rank = models.IntegerField() #how to set this?

	def __unicode__(self):
		return self.option

class Config(models.Model):
	questions = models.ManyToManyField(Question)
	name = models.CharField(max_length=128)
	description = models.TextField(default="")

	def __unicode__(self):
		return self.name
