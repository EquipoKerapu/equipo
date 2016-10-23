from django.test import TestCase
from .models import *
from .views import *
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
import json


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