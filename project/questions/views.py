from .models import Question, Answer, Category, Like
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .forms import QuestionListForm, SignUpForm, AnswerAdd, AskQuestion, UpdateQuestion, LikeForm, ProfileForm
from django.shortcuts import resolve_url, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F


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
    form_class = AskQuestion

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(QuestionCreate, self).form_valid(form)

    def get_success_url(self):
        return resolve_url('question_detail', pk=self.object.pk)


class QuestionUpdate(UpdateView):
    """Страница изменения вопроса"""
    template_name = "question_update.html"
    model = Question
    form_class = UpdateQuestion

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

    def get_queryset(self):
        queryset = Question.objects.all()
        queryset = queryset.annotate(answers_count=Count('answers__id'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(QuestionDetail, self).get_context_data(**kwargs)
        context['answers'] = Answer.objects.filter(question=self.kwargs['pk']).order_by('-created_at')
        context['form'] = self.form
        return context


class QuestionLike(QuestionDetail):
    """Лайк"""
    def dispatch(self, request, *args, **kwargs):
        question = Question.objects.get(pk=self.kwargs['pk'])
        self.like = LikeForm(request.POST)
        try:
            all_likes = Like.objects.filter(question=question)  # Выборка всех лайков к этому вопросу
            own = False
            if all_likes.filter(author=request.user).exists():  # Ищет пользователя в авторах лайков к этому вопросу
                own = True
            if self.like.is_valid() and not own:  # Если пользователь еще не ставил лайк
                q_like = self.like.save(commit=False)
                q_like.author = request.user
                q_like.question = question
                q_like.save()
                question.rating = F('rating') + 1
                question.save()
                question.likes.add(q_like)
                return redirect('question_detail', pk=question.pk)
            elif self.like.is_valid() and own:  # Если пользователь уже ставил лайк
                return redirect('question_detail', pk=question.pk)
        except:
            return redirect('question_detail', pk=question.pk)
        return super(QuestionDetail, self).dispatch(request, *args, **kwargs)


class QuestionList(ListView):
    """Страница со всеми вопросами"""
    template_name = "question_list.html"
    model = Question
    paginate_by = 20

    def dispatch(self, request, *args, **kwargs):
        self.form = QuestionListForm(request.GET)
        self.form.is_valid()
        return super(QuestionList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
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
        return context


class Index(TemplateView):
    """Главная страница"""
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['popular_questions'] = Question.objects.exclude(rating__lt=1).annotate(answers_count=Count('answers__id')).order_by('-rating')[:10]
        return context


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
        context['questions'] = Question.objects.filter(categories=self.kwargs['pk']).annotate(answers_count=Count('answers__id')).order_by('-created_at')
        return context


class QuestionCommentAjax(DetailView):
    """Комментарии к вопросу"""
    model = Question
    template_name = "question_comment_ajax.html"

    def get_context_data(self, **kwargs):
        context = super(QuestionCommentAjax, self).get_context_data(**kwargs)
        context['answers'] = Answer.objects.filter(question=self.kwargs['pk']).order_by('-created_at')
        return context


class UserProfile(ListView):
    """Страница профиля пользователя"""
    model = User
    template_name = "profile.html"

    def get_queryset(self):
        return super(UserProfile, self).get_queryset().filter(username=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        context['questions_all'] = Question.objects.filter(author=self.request.user).annotate(answers_count=Count('answers__id')).order_by('-created_at')
        return context


@login_required
def update_profile(request):
    """Редактирование профиля"""
    if request.method == 'POST':
        user_form = SignUpForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('/index/')
    else:
        user_form = SignUpForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })