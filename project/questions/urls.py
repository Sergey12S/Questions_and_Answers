from django.conf.urls import url
from questions.views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$', QuestionList.as_view()),
    url(r'^(?P<pk>\d+)/$', QuestionDetail.as_view(), name='question_detail'),
    url(r'^create/$', login_required(QuestionCreate.as_view())),
    url(r'^(?P<pk>\d+)/update/$', QuestionUpdate.as_view(), name='question_update'),
    url(r'^(?P<pk>\d+)/delete/$', QuestionDelete.as_view(), name='question_delete'),
    url(r'^categories/$', CategoriesList.as_view(), name='categories_list'),
    url(r'^categories/(?P<pk>\d+)/$', CategoriesDetail.as_view(), name='categories_detail'),
    url(r'^(?P<pk>\d+)/ajax/$', QuestionCommentAjax.as_view(), name='question_comments'),
    url(r'^(?P<pk>\d+)/like/$', QuestionLike.as_view(), name='question_like'),
]