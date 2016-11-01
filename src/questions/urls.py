from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^questions/?$', QuestionListView.as_view(), name='question-list'),
    url(r'^questions/(?P<pk>\d+)/?$', QuestionDetailView.as_view(), name='question-detail'),
]