from django import forms
from .models import Question
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Answer


class SignUpForm(UserCreationForm):
    """Регистрация пользователя"""
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


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

    """
    def clean_search(self):
        search = self.cleaned_data.get('search')
        raise forms.ValidationError(u'Я неправильный поиск!')
        return search
    """


"""
class QuesForm(forms.Form):

    title = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea)
"""
