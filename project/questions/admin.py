from django.contrib import admin
from .models import Question, Answer, Category, Like


admin.site.register(Question)

admin.site.register(Answer)

admin.site.register(Category)

admin.site.register(Like)