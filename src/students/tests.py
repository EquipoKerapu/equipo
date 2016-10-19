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
		self.student = Student.objects.create(first_name='Test',
										last_name='User')

	def test_student_user(self):
		self.student.set_user(username='test_user', password='test_user_pwd')
		self.assertEqual(self.student.user.username, 'test_user')
		self.assertFalse(self.student.user.is_superuser)
		self.assertFalse(self.student.user.is_staff)

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

	def list_students(self):
		request = self.factory.get(self.student_api)
		request.user = self.user
		response = StudentListCreateView.as_view()(request)
		response = response.render()
		return json.loads(response.content)

	def test_student_list_api(self):
		res = self.list_students()
		self.assertIsInstance(res, list)
		self.assertEqual(len(res), 0)

		Student.objects.create(first_name="test", last_name="user")

		res = self.list_students()
		self.assertIsInstance(res, list)
		self.assertEqual(len(res), 1)

