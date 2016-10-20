from django.shortcuts import render
from rest_framework import generics
from .models import Student
from .serializers import StudentSerializer, StudentCreateUpdateSerializer
from rest_framework.permissions import SAFE_METHODS
# Create your views here.

class StudentListCreateView(generics.ListCreateAPIView):
	queryset = Student.objects.all()
	serializer_class = StudentSerializer

	def get_serializer(self, *args, **kwargs):
		print kwargs
		method = self.request.method
		serializer = super(StudentListCreateView, self).get_serializer_class()
		if method in SAFE_METHODS:
			return serializer(*args, **kwargs)
		else:
			return StudentCreateUpdateSerializer(*args, **kwargs)

class StudentRetrieveUpdateView(generics.RetrieveUpdateAPIView):
	queryset = Student.objects.all()
	serializer_class = StudentSerializer

	def get_serializer(self, *args, **kwargs):
		method = self.request.method
		serializer = super(StudentRetrieveUpdateView, self).get_serializer_class()
		if method in SAFE_METHODS:
			return serializer(*args, **kwargs)
		else:
			return StudentCreateUpdateSerializer(*args, **kwargs)


