from django.test import TestCase
from .models import *
from .views import *
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
import json
from django.core import management


# Create your tests here.
class StudentModelTestCase(TestCase):
	def setUp(self):
		self.student = Student.objects.create()

	def test_student_user(self):
		self.student.create_user(username='test_user', password='test_user_pwd', email="eahuntington@cpp.edu")
		self.assertEqual(self.student.user.username, 'test_user')
		self.assertFalse(self.student.user.is_superuser)
		self.assertFalse(self.student.user.is_staff)

	def test_student_user_kwargs(self):
		self.student.create_user(username='test_user', password='test_user_pwd', email="eahuntington@cpp.edu", kwargs={'first_name': 'elinor', 'last_name': 'huntington'})

	def test_student_courses(self):
		course1 = Course.objects.create(course_title="title", 
										course_number='CS1000', 
										course_quarter="Fall", 
										course_year=2000)
		StudentCourseMapping.objects.create(course=course1, student=self.student)
		self.assertIn(course1.course_title, self.student.courses.values_list('course_title', flat=True))

class StudentAPITestCase(APITestCase):
	def setUp(self):
		self.factory = APIRequestFactory()
		self.student_api = '/students'
		self.user = User.objects.create(username='superuser')
		self.user.is_superuser = True
	
	def render_response(self, response):
		response = response.render()
		return json.loads(response.content), response.status_code

	def get_student(self, pk):
		request = self.factory.get("{0}/{1}".format(self.student_api, pk))
		request.user = self.user
		response = StudentRetrieveUpdateView.as_view()(request, pk=pk)
		return self.render_response(response)

	def post_student(self, student_json):
		request = self.factory.post(self.student_api, student_json)
		request.user = self.user
		response = StudentListCreateView.as_view()(request)
		return self.render_response(response)

	def put_student(self, student_json, pk):
		request = self.factory.put("{0}/{1}".format(self.student_api, pk), student_json)
		request.user = self.user
		response = StudentRetrieveUpdateView.as_view()(request, pk=pk)
		return self.render_response(response)
		
	def list_students(self):
		request = self.factory.get(self.student_api)
		request.user = self.user
		response = StudentListCreateView.as_view()(request)
		return self.render_response(response)

	def test_student_list_api(self):
		res, st = self.list_students()
		self.assertIsInstance(res, list)
		self.assertEqual(len(res), 0)

		Student.objects.create(first_name="test", last_name="user")

		res, st = self.list_students()
		self.assertIsInstance(res, list)
		self.assertEqual(len(res), 1)
		
	def test_student_post_api(self):
		user = User.objects.create(first_name='bob', last_name='snob')
		student_json = {"user": user.id}

		res, st = self.post_student(student_json)
		self.assertEqual(st, 201)

	def test_student_put_api(self):
		user = User.objects.create(first_name='bob', last_name='snob')
		student_json = {"user": user.id}
		res, st = self.post_student(student_json)
		self.assertEqual(st, 201)
		self.assertEqual(res['user']['first_name'], 'bob')

		updated_student_json = {"id": res['id'], "first_name": "bob is updated", "last_name": "snob", "user": user.id}
		res, st = self.put_student(updated_student_json, res['id'])
		self.assertEqual(st, 200)
		self.assertEqual(res['user']['first_name'], "bob is updated")

	def test_student_get_api(self):
		user = User.objects.create()
		student_json = {"first_name": "bob", "last_name": "snob", "user": user.id}
		res, st = self.post_student(student_json)
		self.assertEqual(st, 201)
		self.assertEqual(res['first_name'], 'bob')

		res, st = self.get_student(res['id'])
		self.assertEqual(st, 200)
		self.assertEqual(res['first_name'], 'bob')

class IntegrationTestCase(TestCase):
	def setUp(self):
		#superuser = SiteUser.objects.create()
		#superuser.create_user(username="superuser", password="qwertyuiop", email="superuser@cpp.edu", kwargs={'is_superuser':True})

		students = [None]*9
		for i in range(1,10):
			user = User.objects.create(username="student_{}".format(i), password="qwertyuiop", email="stu_{}@cpp.edu".format(i))
			students[i-1] = SiteUser.objects.create(user=user, is_professor=False)

		courses = [None]*3
		for i in range(1,4):
			courses[i-1] = Course.objects.create(course_title="course {}".format(i), course_number=i, course_quarter="Fall", course_year="2016")

		professors = [None]*2
		for i in range(1,3):
			user = User.objects.create(username="professor_{}".format(i), password="qwertyuiop", email="prof_{}@cpp.edu".format(i))
			professors[i-1] = SiteUser.objects.create(user=user, is_professor=True)

		questions = [None]*9
		options = []
		for i in range(1,10):
			questions[i-1] = Question.objects.create(question="Is {}?".format(i), relative_weight=i)
			for j in range(1,4):
				options.append(Option.objects.create(rank=i, option="opt {0}-{1}".format(i, j), question=questions[i-1]))
		self.students = SiteUser.objects.filter(is_professor=False)
		self.assertEqual(len(self.students), 9)
		self.courses = Course.objects.all()
		self.professors = SiteUser.objects.filter(is_professor=True)
		self.questions = Question.objects.all()
		self.options = Option.objects.all()


		pcm_1 = ProfessorCourseMapping.objects.create(professor=self.professors[0], course=self.courses[0])
		pcm_1.questions = [q.id for q in self.questions[0:3]]

		for q in pcm_1.questions.all():
			print q.question_options.all()

		pcm_2 = ProfessorCourseMapping.objects.create(professor=self.professors[0], course=self.courses[1])
		pcm_2.questions = [q.id for q in self.questions[3:6]]

		for q in pcm_2.questions.all():
			print q.question_options.all()

		pcm_3 = ProfessorCourseMapping.objects.create(professor=self.professors[1], course=self.courses[2])
		pcm_3.questions = [q.id for q in self.questions[6:]]

		for q in pcm_3.questions.all():
			print q.question_options.all()

		scms = []
		for i in range(0,9):
			scms.append(StudentCourseMapping.objects.create(student=self.students[i], course=self.courses[i%3]))

		for scm in scms:
			print scm.student
			print scm.course
			course_questions = ProfessorCourseMapping.objects.get(course=scm.course).questions.all()
			#print course_questions
			for course_question in course_questions:
				print course_question
				print course_question.question_options.all()
				scm.options.add(course_question.question_options.all()[0])
			print scm.options.all()
			print "_________________________"
	def test_one(self):
		print self.students
		print self.courses
		print self.professors
		print self.questions
		print self.options

		management.call_command('dumpdata', output="students/fixtures/test_fixture.json", 
							indent=4, use_natural_foreign=True)



