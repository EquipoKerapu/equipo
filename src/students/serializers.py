from rest_framework import serializers
from .models import Student
from courses.serializers import CourseSerializer
from django.contrib.auth.models import User
from courses.models import Course

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User

class StudentSerializer(serializers.ModelSerializer):
	courses = CourseSerializer(many=True)
	user = UserSerializer()
	class Meta:
		model = Student 
		fields = ('id', 'user', 'first_name', 'last_name', 'courses')

class StudentCreateUpdateSerializer(serializers.ModelSerializer):
	#courses = serializers.ListField(serializers.IntegerField()) #need to figure this out
	user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
	def save_student(self, validated_data, instance=None):
		if instance is None:
			# create
			instance = Student(**validated_data)
			instance.save()
		else:
			# update
			for attr in validated_data:
				setattr(instance, attr, validated_data[attr])
			instance.save()	

		return instance

	def create(self, validated_data):
		return self.save_student(validated_data)

	def update(self, instance, validated_data):
		return self.save_student(validated_data, instance)

	class Meta:
		model = Student
		fields = ('id', 'user',  'first_name', 'last_name')

