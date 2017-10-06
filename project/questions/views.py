from .models import Question, Answer, Category
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import QuestionListForm, SignUpForm, AnswerAdd
from django.shortcuts import resolve_url, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count


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
    fields = ('title', 'text', 'categories')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(QuestionCreate, self).form_valid(form)

    def get_success_url(self):
        return resolve_url('question_detail', pk=self.object.pk)


class QuestionUpdate(UpdateView):
    """Страница изменения вопроса"""
    template_name = "question_update.html"
    model = Question
    fields = ('categories', 'title', 'text')

    def get_queryset(self):
        return super(QuestionUpdate, self).get_queryset().filter(author=self.request.user)

    def get_success_url(self):
        return resolve_url('question_detail', pk=self.object.pk)


class QuestionDelete(DeleteView):
    """Страница удаления вопроса"""
    model = Question
    template_name = "question_delete.html"
    success_url = '/index/'

    def get_queryset(self):
        return super(QuestionDelete, self).get_queryset().filter(author=self.request.user)


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
        queryset = queryset.annotate(answers_count=Count('answers__id'))
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


class CategoriesList(ListView):
    """Страница со списком категорий"""
    model = Category
    template_name = "categories_list.html"


class CategoriesDetail(DetailView):
    """Страница категории детально"""
    model = Category
    template_name = "categories_detail.html"

    def get_context_data(self, **kwargs):
        context = super(CategoriesDetail, self).get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(categories=self.kwargs['pk']).order_by('-created_at')
        return context