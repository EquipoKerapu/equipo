from rest_framework import serializers
from .models import Student
from courses.serializers import CourseSerializer
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User

class StudentSerializer(serializers.ModelSerializer):
	courses = CourseSerializer(many=True)
	user = UserSerializer()
	class Meta:
		model = Student 
		fields = ('id', 'user', 'first_name', 'last_name', 'courses')