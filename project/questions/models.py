from django.db import models
from django.conf import settings


class Category(models.Model):

    name = models.CharField(verbose_name=u'название', max_length=50)

    class Meta:
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'

    def __str__(self):
        return self.name


class Question(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=255, verbose_name=u'заголовок')
    text = models.TextField(verbose_name=u'описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'дата создания')
    rating = models.IntegerField(default=0, verbose_name=u'рейтинг')
    categories = models.ManyToManyField(Category, related_name='questions')
    likes = models.ManyToManyField('questions.Like', related_name='qlikes', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'Вопрос'
        verbose_name_plural = u'Вопросы'
        ordering = ('-created_at', )


class Answer(models.Model):

    question = models.ForeignKey(Question, related_name='answers')
    text = models.TextField(verbose_name=u'ответ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'дата создания')
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = u'Ответ'
        verbose_name_plural = u'Ответы'


class Like(models.Model):

    title = models.CharField(verbose_name=u'название', max_length=10, default=u'лайк', blank=True)
    question = models.ForeignKey(Question, related_name='likeq')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'дата создания')
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u'Лайк'
        verbose_name_plural = u'Лайки'
