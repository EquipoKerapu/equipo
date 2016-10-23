from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Question(models.Model):
	question = models.TextField()
	relative_weight = models.IntegerField(choices=[(i,i) for i in range(1,11)])

	def __unicode__(self):
		return self.question

class Option(models.Model):
	question = models.ForeignKey(Question)
	option = models.TextField()
	rank = models.IntegerField() #how to set this?

	def __unicode__(self):
		return self.option