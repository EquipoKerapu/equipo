from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
from questions.models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Permission
from django.db.models import Q

class SiteUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='site_user')
	is_professor = models.BooleanField(default=False)

	def __unicode__(self):
		return self.user.username

	def save(self, *args, **kwargs):
		if self.is_professor:
			perms = Permission.objects.all()
			question_perms = perms.filter(codename__contains="question")
			option_perms = perms.filter(codename__contains="option")
			config_perms = perms.filter(codename__contains="config")
			course_perms = perms.filter(Q(codename__contains="course") & ~Q(codename__contains="student"))
			for perm_list in (question_perms, option_perms, config_perms, course_perms):
				for permission in perm_list:
					self.user.user_permissions.add(permission)
			self.user.save()
		self.user.save()
		super(SiteUser, self).save(*args, **kwargs)

	class Meta:
		app_label = "students"

class StudentCourseMapping(models.Model):
	student = models.ForeignKey(SiteUser, related_name="student_courses")
	course = models.ForeignKey(Course, related_name="student_mapping")
	rank = models.IntegerField(null=True, blank=True)# Do we need this to persist here?
	options = models.ManyToManyField(Option)

	def __unicode__(self):
		return "{0}:{1}".format(self.student.user.username, self.course.course_title)

	class Meta:
		unique_together = ('student', 'course')

class ProfessorCourseMapping(models.Model):
	professor = models.ForeignKey(SiteUser, related_name="professor_courses")
	course = models.OneToOneField(Course, related_name="professor_mapping")
	config = models.ForeignKey(Config, null=True)

	def __unicode__(self):
		return "{0}:{1}".format(self.professor.user.username, self.course.course_title)

	class Meta:
		unique_together = ('professor', 'course')


