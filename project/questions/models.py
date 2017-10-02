from django.db import models
from django.conf import settings


class Question(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'Вопрос'
        verbose_name_plural = u'Вопросы'
        ordering = ('-created_at', )
