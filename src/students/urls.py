from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^students/?$', StudentListView.as_view(), name='student-list'),
    url(r'^students/(?P<pk>\d+)/?$', StudentDetailView.as_view(), name='student-detail'),
]
