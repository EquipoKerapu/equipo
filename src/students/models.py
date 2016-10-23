from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
from questions.models import *
from django.core.exceptions import ValidationError

# Create your models here.

class SiteUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	is_professor = models.BooleanField(default=False)

	def create_user(self, username, password, email, **kwargs):
		user = User.objects.create(username=username, password=password, email=email)
		for attr in kwargs:
			setattr(user, attr, kwargs[attr])
		self.user = user

	def __unicode__(self):
		return self.user.username

class StudentCourseMapping(models.Model):
	student = models.ForeignKey(SiteUser, related_name="student_courses")
	course = models.ForeignKey(Course)
	rank = models.IntegerField(null=True, blank=True)# Do we need this to persist here?
	options = models.ManyToManyField(Option)

	def __unicode__(self):
		return "{0}:{1}".format(self.student.user.username, self.course.course_title)

class ProfessorCourseMapping(models.Model):
	professor = models.ForeignKey(SiteUser, related_name="professor_courses")
	course = models.ForeignKey(Course)
	questions = models.ManyToManyField(Question)

	def __unicode__(self):
		return "{0}:{1}".format(self.professor.user.username, self.course.course_title)