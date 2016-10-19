from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
from django.core.exceptions import ValidationError

# Create your models here.

class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	first_name = models.CharField(max_length=64, blank=True)
	last_name = models.CharField(max_length=64, blank=True)
	courses = models.ManyToManyField(Course, through='StudentCourseMapping')

	def set_user(self, username, password):
		user = User.objects.create(username=username, password=password)
		self.user = user

class StudentCourseMapping(models.Model):
	student = models.ForeignKey(Student)
	course = models.ForeignKey(Course)
	rank = models.IntegerField(null=True, blank=True)# Do we need this to persist here?


