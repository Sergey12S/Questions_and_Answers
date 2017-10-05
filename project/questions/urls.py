from django.conf.urls import url
from .views import QuestionList, QuestionDetail, QuestionCreate, QuestionUpdate, QuestionDelete
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$', QuestionList.as_view()),
    url(r'^(?P<pk>\d+)/$', QuestionDetail.as_view(), name='question_detail'),
    url(r'^create/$', login_required(QuestionCreate.as_view())),
    url(r'^(?P<pk>\d+)/update/$', QuestionUpdate.as_view(), name='question_update'),
    url(r'^(?P<pk>\d+)/delete/$', QuestionDelete.as_view(), name='question_delete')
]