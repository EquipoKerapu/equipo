from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
	FALL = 'Fall'
	WINTER = 'Winter'
	SPRING = 'Spring'
	SUMMER = 'Summer'
	QUARTER_CHOICES = (
		(FALL, 'Fall'),
		(WINTER, 'Winter'),
		(SPRING, 'Spring'),
		(SUMMER, 'Summer'),
		)
	course_title = models.CharField(max_length=64)
	course_number = models.CharField(max_length=16)
	course_quarter = models.CharField(max_length=16, choices=QUARTER_CHOICES)
	course_year = models.IntegerField()

	created_by = models.ForeignKey(User, null=True)
	created_on = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return "{0}: {1}, {2} {3}".format(self.course_number, self.course_title, self.course_quarter, self.course_year)
