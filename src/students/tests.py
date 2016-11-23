from django.test import TestCase
from students.models import *
from students.views import *
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
import json
import csv
import random
from django.core import management

from django.contrib.auth.models import Permission

from django.db.models import Q

def questions_options():
	general_options = ['Coursework Only', 'Intership, less than 3 months', 'Intership, more than 3 months', 'Professional Experience, less than 1 year', 'Professional Experience, more than 1 year']
	standard_options = ['None', 'Novice', 'Intermediate', 'Expert']
	time_options = ['None', '> 3 months', '3 months to 6 months', '6 months to a year', '2 years', 'more than 2 years']

	general_questions = ["How much work experience do you have that is related to CS?"]

	languages = ['Javascript', 'Java', 'HTML', 'CSS', 'Python', 'C', 'C++']
	frameworks = ['Spring', 'Django', 'AngularJS', 'Ruby on Rails']
	databases = [ 'MySQL', 'PostgreSQL', 'MongoDB', 'Microsoft SQL Server']

	language_length_questions = ["How much time have you spent programming in {}".format(x) for x in languages]
	language_level_questions = ["What would you say your experience level in {} is?".format(x) for x in languages]

	framework_length_questions = ["How much time have you spent working with {}?".format(x) for x in frameworks]
	framework_level_questions = ["What would you say your experience level in {} is?".format(x) for x in frameworks]

	database_length_questions = ["How much time have you spent working with {}?".format(x) for x in databases]
	database_level_questions = ["What would you say your experience level in {} is?".format(x) for x in databases]

	questions = [
			[language_level_questions, framework_level_questions, database_level_questions],
			[language_length_questions, framework_length_questions, database_length_questions],
			[general_questions]
	]
	options = [standard_options, time_options, general_options]

	return questions, options


def process_lists(lists, options, weight_lambda, rank_lambda):
	config_questions = []
	for q_list in lists:
		i = 1
		for q in q_list:
			question = Question.objects.create(question_text=q, relative_weight=weight_lambda(i))
			j = 1
			for o in options:
				Option.objects.create(rank=rank_lambda(j), option=o, question=question)
				j += 1
			i += 1
			config_questions.append(question)	
	return config_questions

def create_config(config_name, questions_and_options, professor, course_title, weight_lambda, rank_lambda):
	'''Creates a configuration 

	Keyword arguments
	config_name -- config name for create (string)
	questions_and_options -- a zipped tuple of lists of questions and attendant options (tuple)
	professor -- professor username for get (string)
	course_title -- course title for get (string)

	'''
	config = Config.objects.create(name=config_name)
	config_questions = []
	for q_and_o in questions_and_options:
		config_questions += process_lists(q_and_o[0], q_and_o[1], weight_lambda, rank_lambda)
	config.questions = [q.id for q in config_questions]
	prof = SiteUser.objects.get(is_professor=True, user__username=professor)
	course = Course.objects.get(course_title=course_title)
	pcm = ProfessorCourseMapping.objects.create(professor=prof, course=course)
	pcm.config = config 
	pcm.save()
	return config

def coerce_boolean(value):
	if value == "TRUE":
		return True 
	return False

def create_users():
	with open('students/test_data/users.csv', 'rb') as f:
		reader = csv.reader(f)
		rownum = 0
		for row in reader:
			if rownum > 0:
				user = User.objects.create(username=row[2], email=row[3])
				user.set_password(row[4])
				user.is_staff = coerce_boolean(row[5])
				SiteUser.objects.create(user=user, is_professor=coerce_boolean(row[6]))
			rownum += 1

def create_courses():
	with open('students/test_data/courses.csv', 'rb') as f:
		reader = csv.reader(f)
		rownum = 0
		for row in reader:
			if rownum > 0:
				Course.objects.create(course_title=row[0], course_number=row[1], course_quarter=row[2], course_year=row[3])			
			rownum += 1


class DemoTestCase(TestCase):

	def setUp(self):
		create_users()
		create_courses()

		#config 1 - all questions have the same weight; options increment weight by 1
		questions, options = questions_options()
		questions_and_options = zip(questions, options)
		config_1 = create_config("Configuration 1", questions_and_options, 'bhall', 'Software Engineering', lambda x:1, lambda y:y)
		#config 2 - questions ordered in descending weight, lowest=1, options increment by i^2 + 1
		questions_and_options = zip([questions[0]], [options[0]])
		config_2 = create_config("Configuration 2", questions_and_options, 'bhall', 'Operating Systems', lambda x: 10-x, lambda y:y**2 + 1)
		#config 3 - all questions have same weight, options increment by i^2 + i
		questions_and_options = zip(questions[1:], options[1:])	
		config_3 = create_config("Configuration 3", questions_and_options, 'sperez', 'Compilers and Interpreters', lambda x:2, lambda y:y**2 + y)

	def test_one(self):
		'''
		all configs set up and student answers randomly assigned
		'''
		students = SiteUser.objects.filter(is_professor=False)
		professors = SiteUser.objects.filter(is_professor=True)
		courses = Course.objects.all()
		config_1 = Config.objects.get(name="Configuration 1")
		config_2 = Config.objects.get(name="Configuration 2")
		config_3 = Config.objects.get(name="Configuration 3")

		self.assertEqual(len(students), 36)
		self.assertEqual(len(professors), 2)
		self.assertEqual(len(courses), 3)
		self.assertEqual(len(config_1.questions.all()), 31)
		self.assertEqual(len(config_2.questions.all()), 15)
		self.assertEqual(len(config_3.questions.all()), 16)

		scms = []
		for student in students:
			for course in courses:
				scms.append(StudentCourseMapping.objects.create(student=student, course=course))

		for scm in scms:
			course_questions = ProfessorCourseMapping.objects.get(course=scm.course).config.questions.all()
			for q in course_questions:
				options = q.question_options.all()
				scm.options.add(options[random.randint(0, len(options) - 1)])

		management.call_command('dumpdata', output="students/fixtures/demo_fixture.json", 
							indent=4, use_natural_foreign=True)

	def test_two(self):


		students = SiteUser.objects.filter(is_professor=False)
		professors = SiteUser.objects.filter(is_professor=True)
		courses = Course.objects.all()
		config_1 = Config.objects.get(name="Configuration 1")
		config_2 = Config.objects.get(name="Configuration 2")
		config_3 = Config.objects.get(name="Configuration 3")

		self.assertEqual(len(students), 36)
		self.assertEqual(len(professors), 2)
		self.assertEqual(len(courses), 3)
		self.assertEqual(len(config_1.questions.all()), 31)
		self.assertEqual(len(config_2.questions.all()), 15)
		self.assertEqual(len(config_3.questions.all()), 16)

		management.call_command('dumpdata', output="students/fixtures/demo_fixture_noscms.json", 
							indent=4, use_natural_foreign=True)

class PermissionsTestCase(TestCase):
	def setUp(self):
		self.prof = User.objects.create(username="professor")
		self.prof_su = SiteUser.objects.create(user=self.prof, is_professor=True)
		self.stu = User.objects.create(username="student")
		self.stu_su = SiteUser.objects.create(user=self.stu, is_professor=False)

		self.perm_codenames = ["add_course", "change_course", "delete_course", "add_config", "change_config", "delete_config",
								"add_option", "change_option", "delete_option", "add_question", "change_question",
								"delete_question", "add_professorcoursemapping", "change_professorcoursemapping",
								"delete_professorcoursemapping"]

	def test_prof_permissions(self):
		perms = Permission.objects.filter(user=self.prof)
		for perm in perms:
			self.assertIn(perm.codename, self.perm_codenames)
		self.assertTrue(len(perms) == 15)

	def test_stu_permissions(self):
		perms = Permission.objects.filter(user=self.stu)
		self.assertTrue(len(perms) == 0)		

class IntegrationTestCase(TestCase):
	def setUp(self):
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



