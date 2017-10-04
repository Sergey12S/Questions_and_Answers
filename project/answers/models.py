from django.db import models
from django.conf import settings
from questions.models import Question


class Answer(models.Model):

    question = models.ForeignKey(Question, related_name='answers')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        verbose_name = u'Ответ'
        verbose_name_plural = u'Ответы'
