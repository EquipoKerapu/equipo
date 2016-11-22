from django.test import TestCase
from students.models import *
from students.views import *
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
import json
from django.core import management

from django.contrib.auth.models import Permission

from django.db.models import Q

class IntegrationTestCase(TestCase):
	def setUp(self):
		#superuser = SiteUser.objects.create()
		#superuser.create_user(username="superuser", password="qwertyuiop", email="superuser@cpp.edu", kwargs={'is_superuser':True})

		perms = Permission.objects.all()

		students = [None]*9
		for i in range(1,10):
			user = User.objects.create(username="student_{}".format(i),email="stu_{}@cpp.edu".format(i))
			user.set_password("qwertyuiop")
			user.is_staff = False
			user.save()
			students[i-1] = SiteUser.objects.create(user=user, is_professor=False)

		courses = [None]*3
		for i in range(1,4):
			courses[i-1] = Course.objects.create(course_title="course {}".format(i), course_number=i, course_quarter="Fall", course_year="2016")

		professors = [None]*2
		for i in range(1,3):
			user = User.objects.create(username="professor_{}".format(i), email="prof_{}@cpp.edu".format(i))
			user.set_password("qwertyuiop")
			user.is_staff = True
			question_perms = perms.filter(codename__contains="question")
			option_perms = perms.filter(codename__contains="option")
			config_perms = perms.filter(codename__contains="config")
			course_perms = perms.filter(Q(codename__contains="course") & ~Q(codename__contains="student"))
			for perm_list in (question_perms, option_perms, config_perms, course_perms):
				for permission in perm_list:
					user.user_permissions.add(permission)

			user.save()
			professors[i-1] = SiteUser.objects.create(user=user, is_professor=True)

		
		config_1 = Config.objects.create()
		config_2 = Config.objects.create()
		config_3 = Config.objects.create()

		questions = [None]*9
		options = []
		for i in range(1,10):
			questions[i-1] = Question.objects.create(question_text="Is {}?".format(i), relative_weight=i)
			for j in range(1,4):
				options.append(Option.objects.create(rank=i, option="opt {0}-{1}".format(i, j), question=questions[i-1]))
		self.students = SiteUser.objects.filter(is_professor=False)
		self.assertEqual(len(self.students), 9)
		self.courses = Course.objects.all()
		self.professors = SiteUser.objects.filter(is_professor=True)
		self.questions = Question.objects.all()
		self.options = Option.objects.all()


		config_1.questions = [q.id for q in self.questions[0:3]]
		config_2.questions = [q.id for q in self.questions[3:6]]
		config_3.questions = [q.id for q in self.questions[6:]]

		pcm_1 = ProfessorCourseMapping.objects.create(professor=self.professors[0], course=self.courses[0])
		pcm_1.config = config_1
		pcm_1.save()

		pcm_2 = ProfessorCourseMapping.objects.create(professor=self.professors[0], course=self.courses[1])
		pcm_2.config = config_2
		pcm_2.save()

		pcm_3 = ProfessorCourseMapping.objects.create(professor=self.professors[1], course=self.courses[2])
		pcm_3.config = config_3
		pcm_3.save()

		scms = []
		for i in range(0,9):
			scms.append(StudentCourseMapping.objects.create(student=self.students[i], course=self.courses[i%3]))

		for scm in scms:
			course_questions = ProfessorCourseMapping.objects.get(course=scm.course).config.questions.all()
			for course_question in course_questions:
				scm.options.add(course_question.question_options.all()[0])

	def test_one(self):
		management.call_command('dumpdata', output="students/fixtures/test_fixture.json", 
							indent=4, use_natural_foreign=True)



