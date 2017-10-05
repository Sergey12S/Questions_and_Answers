from .models import Question
from .models import Answer
from django.views.generic import ListView, DetailView, CreateView
from .forms import QuestionListForm, SignUpForm, AnswerAdd
# from .forms import QuesForm
from django.shortcuts import resolve_url, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


class SignUp(CreateView):
    """Страница регистрации"""
    model = User
    template_name = "sign_up.html"
    form_class = SignUpForm
    success_url = "/index/"


class QuestionCreate(CreateView):
    """Страница создания вопроса"""
    model = Question
    template_name = "question_create.html"
    fields = ('title', 'text')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(QuestionCreate, self).form_valid(form)

    def get_success_url(self):
        return resolve_url('question_detail', pk=self.object.pk)


class QuestionDetail(DetailView):
    """Детальная страница с вопросом и ответами"""
    template_name = "question_detail.html"
    model = Question

    def dispatch(self, request, *args, **kwargs):
        question = Question.objects.get(pk=self.kwargs['pk'])
        self.form = AnswerAdd(request.POST)
        try:
            if self.form.is_valid():
                answer = self.form.save(commit=False)
                answer.author = request.user
                answer.question = question
                answer.save()
                return redirect('question_detail', pk=question.pk)
        except:
             return redirect('question_detail', pk=question.pk)
        return super(QuestionDetail, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(QuestionDetail, self).get_context_data(**kwargs)
        context['answers'] = Answer.objects.filter(question=self.kwargs['pk']).order_by('-created_at')
        context['form'] = self.form
        return context


class QuestionList(ListView):
    """Страница со всеми вопросами"""
    template_name = "question_list.html"
    model = Question
    paginate_by = 20

    def dispatch(self, request, *args, **kwargs):
        self.form = QuestionListForm(request.GET)
        self.form.is_valid()
        # self.qform = QuesForm(request.POST or None)
        return super(QuestionList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # queryset = Question.objects.filter(author=self.request.user)Показывает вопросы залогиненого юзера
        queryset = Question.objects.all()
        if self.form.cleaned_data.get('search'):
            queryset = queryset.filter(title=self.form.cleaned_data['search'])
        if self.form.cleaned_data.get('sort_field'):
            queryset = queryset.order_by(self.form.cleaned_data['sort_field'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(QuestionList, self).get_context_data(**kwargs)
        context['form'] = self.form
        # context['qform'] = self.qform
        return context


class Index(QuestionList):
    """Главная страница"""
    model = Question
    template_name = "index.html"

    def get_queryset(self):
        return super(Index, self).get_queryset().exclude(rating__lt=10)
