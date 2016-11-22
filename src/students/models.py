from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
from questions.models import *
from django.core.exceptions import ValidationError

# Create your models here.

class SiteUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	is_professor = models.BooleanField(default=False)

	def __unicode__(self):
		return self.user.username

	class Meta:
		app_label = "students"

class StudentCourseMapping(models.Model):
	student = models.ForeignKey(SiteUser, related_name="student_courses")
	course = models.ForeignKey(Course)
	rank = models.IntegerField(null=True, blank=True)# Do we need this to persist here?
	options = models.ManyToManyField(Option)

	def __unicode__(self):
		return "{0}:{1}".format(self.student.user.username, self.course.course_title)

	class Meta:
		unique_together = ('student', 'course')

class ProfessorCourseMapping(models.Model):
	professor = models.ForeignKey(SiteUser, related_name="professor_courses")
	course = models.OneToOneField(Course)
	config = models.ForeignKey(Config, null=True)

	def __unicode__(self):
		return "{0}:{1}".format(self.professor.user.username, self.course.course_title)

	class Meta:
		unique_together = ('professor', 'course')


