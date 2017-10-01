from .models import Question
from django.views.generic import ListView, DetailView, CreateView
from .forms import QuestionListForm, QuesForm, SignInForm
from django.shortcuts import resolve_url
from django.contrib.auth.models import User


class SignIn(CreateView):

    model = User
    template_name = "sign_in.html"
    form_class = SignInForm
    success_url = "/questions/"


class QuestionCreate(CreateView):

    model = Question
    template_name = "question_create.html"
    fields = ('title', 'text')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(QuestionCreate, self).form_valid(form)

    def get_success_url(self):
        return resolve_url('question_detail', pk=self.object.pk)


class QuestionDetail(DetailView):

    template_name = "question_detail.html"
    model = Question


class QuestionList(ListView):

    template_name = "question_list.html"
    model = Question

    def dispatch(self, request, *args, **kwargs):
        self.form = QuestionListForm(request.GET)
        self.form.is_valid()
        self.qform = QuesForm(request.POST or None)
        return super(QuestionList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        #queryset = Question.objects.filter(author=self.request.user)Показывает вопросы залогиненого юзера
        queryset = Question.objects.all()
        if self.form.cleaned_data.get('search'):
            queryset = queryset.filter(title=self.form.cleaned_data['search'])
        if self.form.cleaned_data.get('sort_field'):
            queryset = queryset.order_by(self.form.cleaned_data['sort_field'])[:10]
        return queryset

    def get_context_data(self, **kwargs):
        context = super(QuestionList, self).get_context_data(**kwargs)
        context['form'] = self.form
        context['qform'] = self.qform
        return context
