from django import forms
from .models import Question
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class QuestionListForm(forms.Form):

    search = forms.CharField(required=False)
    sort_field = forms.ChoiceField(choices=(('id', 'ID'), ('created_at', u'Дата создания'),
                                            ('title', u'Заголовок')), required=False)

    """
    def clean_search(self):
        search = self.cleaned_data.get('search')
        raise forms.ValidationError(u'Я не правильный поиск!')
        return search
    """


class QuesForm(forms.Form):

    title = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea)


"""   ИЛИ ИСПОЛЬЗУЕМ
class QForm(forms.ModelForm):

    class Meta:
        model = Question
"""


class SignInForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')