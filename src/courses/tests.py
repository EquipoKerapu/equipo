from django.test import TestCase
from .models import *



# Create your tests here.

class CourseModelTestCase(TestCase):
    def setUp(self):
        self.course = Course.objects.create(course_title = 'CS408',
                                            course_number = '1234',
                                            course_quarter = 'Winter',
                                            course_year = '2017')


    def test_course_get(self):
        stud = Course.objects.get(id = self.course.id)
        self.assertEqual(self.course.course_title, stud.course_title)
