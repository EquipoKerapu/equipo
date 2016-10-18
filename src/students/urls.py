from django.conf.urls import url
from .views import StudentListCreateView

urlpatterns = [
    url(r'^students/', StudentListCreateView.as_view(), name='student-list'),
]
