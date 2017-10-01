from django.conf.urls import url
from .views import QuestionList, QuestionDetail, QuestionCreate


urlpatterns = [
    url(r'^$', QuestionList.as_view()),
    url(r'^(?P<pk>\d+)/$', QuestionDetail.as_view(), name='question_detail'),
    url(r'^create/$', QuestionCreate.as_view()),
]