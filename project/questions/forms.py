from django import forms
from .models import Question
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Answer


class AnswerAdd(forms.ModelForm):  # !

    class Meta:
        model = Answer
        fields = ('text',)


class QuestionListForm(forms.Form):

    search = forms.CharField(required=False)
    sort_field = forms.ChoiceField(choices=(('-created_at', 'Новые'), ('created_at', u'Старые'),
                                            ('title', u'Заголовок')), required=False)

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

"""   ИЛИ ИСПОЛЬЗУЕМ
class QForm(forms.ModelForm):

    class Meta:
        model = Question
"""


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')