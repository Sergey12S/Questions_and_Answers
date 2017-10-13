from django import forms
from questions.models import Question, Answer, Like
from user_change_app.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    """Регистрация пользователя"""
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    """Добавление аватара при регистрации"""
    class Meta:
        model = Profile
        fields = ('avatar',)


class LikeForm(forms.ModelForm):
    """Лайк"""
    class Meta:
        model = Like
        fields = ('title',)


class AskQuestion(forms.ModelForm):
    """Добавляет вопрос"""
    class Meta:
        model = Question
        fields = ('title', 'text', 'categories')


class UpdateQuestion(forms.ModelForm):
    """Редактирует вопрос"""
    class Meta:
        model = Question
        fields = ('title', 'text', 'categories')


class AnswerAdd(forms.ModelForm):
    """Добавление комментария к вопросу"""
    class Meta:
        model = Answer
        fields = ('text',)


class QuestionListForm(forms.Form):
    """Поиск и сортировка на странице всеъ вопросов"""
    search = forms.CharField(required=False)
    sort_field = forms.ChoiceField(choices=(('-created_at', u'Новые'), ('created_at', u'Старые'),
                                            ('title', u'Заголовок'), ('-answers_count', u'Кол-во ответов'),
                                            ('-rating', u'Рейтинг')), required=False)
