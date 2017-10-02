from django.conf.urls import url
from .views import QuestionList, QuestionDetail, QuestionCreate
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$', QuestionList.as_view()),
    url(r'^(?P<pk>\d+)/$', QuestionDetail.as_view(), name='question_detail'),
    url(r'^create/$', login_required(QuestionCreate.as_view())),
]