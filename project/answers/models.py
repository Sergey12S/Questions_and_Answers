from django.db import models


class Answer(models.Model):

    question = models.ForeignKey('questions.Question', related_name='answers')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
