from django.db.models.aggregates import Count, Max, Min, Sum
from django.db.models.expressions import Case, When
from django.db.models.query_utils import Q
from django.shortcuts import render, redirect
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.utils import timezone
from .forms import QuestionForm, PollForm, UserCreateForm, UserUpdateForm, AnswerForm
from .models import Poll, Question, PollAndQuestion, User, Answer, UserAnswer


class UserIsHR(UserPassesTestMixin):
    """
    Миксин проверки имеет ли пользователь полномочия HR
    """
    def test_func(self):
        if self.request.user.is_HR or self.request.user.is_staff:
            return True
        else:
            return False

    def handle_no_permission(self):
        if self.request.user.is_anonymous:
            return redirect("/login/")
        return redirect("/")

class Index(TemplateView):
    template_name = "index.html"

class QuestionList(LoginRequiredMixin, UserIsHR, ListView):
    template_name="question_list.html"
    model=Question
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Перечень всех вопросов"
        return context

@login_required
def question_create(request):
    """
    Контроллер добавления вопроса и ответов на него
    """
    if not request.user.is_HR and not request.user.is_staff:
        return redirect("/")
    AnswerFormset = formset_factory(AnswerForm, min_num=4, max_num=4, can_delete=False, can_order=False)
    if request.method == "POST":
        question_form = QuestionForm(request.POST, request.FILES)
        answer_formset = AnswerFormset(request.POST)
        if question_form.is_valid() and answer_formset.is_valid():
            question = question_form.save()
            for answer in answer_formset:
                if answer.cleaned_data["text"]:
                    answer = answer.save(commit=False)
                    answer.question = question
                    answer.save()
            return HttpResponseRedirect(reverse_lazy("main:question_list"))
    else:
        question_form = QuestionForm()
        answer_formset = AnswerFormset()
    return render(request, "question_form.html", {
        "title":"Новый вопрос",
        "button":"Создать",
        "question":question_form,
        "answers":answer_formset
        })

@login_required
def question_update(request, question_id):
    """
    Контроллер изменения вопроса и ответов на него
    """
    if not request.user.is_HR and not request.user.is_staff:
        return redirect("/")
    question = Question.objects.get(pk=question_id)
    AnswerFormset = inlineformset_factory(Question, Answer, form=AnswerForm, extra=4, max_num=4, can_order=False)
    if request.method == "POST":
        question_form = QuestionForm(request.POST, request.FILES, instance=question)
        answer_formset = AnswerFormset(request.POST, instance=question)
        if question_form.is_valid() and answer_formset.is_valid():
            question = question_form.save()
            for answer in answer_formset:
                if "DELETE" in answer.cleaned_data and answer.cleaned_data["DELETE"] and answer.cleaned_data["id"]:
                    answer.cleaned_data["id"].delete()
                elif "text" in answer.cleaned_data and answer.cleaned_data["text"]:
                    answer = answer.save(commit=False)
                    answer.question = question
                    answer.save()
            return HttpResponseRedirect(reverse_lazy("main:question_list"))
    else:
        question_form = QuestionForm(instance=question)
        answer_formset = AnswerFormset(instance=question)
    return render(request, "question_form.html", {
        "title":"Изменить вопрос",
        "button":"Обновить",
        "question":question_form,
        "answers":answer_formset
        })

class QuestionDelete(LoginRequiredMixin, UserIsHR, DeleteView):
    """
    Контроллер удаления вопроса
    """
    template_name="question_confirm_delete.html"
    model=Question
    success_url=reverse_lazy("main:question_list")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Вы хотите удалить вопрос?"
        context["button"] = "Удалить"
        return context

class QuestionDetail(LoginRequiredMixin, UserIsHR, DetailView):
    """
    Контроллер просмотра всех атрибутов вопроса
    """
    template_name="question_detail.html"
    model=Question
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Вопрос"
        context["answers"] = Answer.objects.filter(question=context["question"])
        return context


class PollList(LoginRequiredMixin, UserIsHR, ListView):
    """
    Контроллер вывода списка всех опросов
    """
    template_name="poll_list.html"
    model=Poll
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Перечень всех опросов"
        return context

class PollCreate(LoginRequiredMixin, UserIsHR, CreateView):
    """
    Контроллер создания нового опроса
    """
    template_name="poll_form.html"
    form_class=PollForm
    success_url=reverse_lazy("main:poll_list")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Новый опрос"
        context["button"] = "Создать"
        return context

class PollUpdate(LoginRequiredMixin, UserIsHR, UpdateView):
    """
    Контроллер выполняющий обновление вопроса
    """
    template_name="poll_form.html"
    model=Poll
    form_class=PollForm
    success_url=reverse_lazy("main:poll_list")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Изменить опрос"
        context["button"] = "Обновить"
        return context

class PollDelete(LoginRequiredMixin, UserIsHR, DeleteView):
    """
    Контроллер удаления опроса
    """
    template_name="poll_confirm_delete.html"
    model=Poll
    success_url=reverse_lazy("main:poll_list")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Вы хотите удалить опрос?"
        context["button"] = "Удалить"
        return context

class PollDetail(LoginRequiredMixin, UserIsHR, DetailView):
    """
    Контроллер просмотра всех атрибутов опроса
    """
    template_name="poll_detail.html"
    model=Poll
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Опрос"
        context["questions"] = PollAndQuestion.objects.filter(poll=context["poll"])
        return context

@login_required
def question_choice_list(request, poll_id, question_category):
    """
    Котроллер управления опросами, добавлят или убирает вопрос из опроса, позволяет задать баллы за ответ на вопрос
    Фильтрация вопросов по типу
    """
    vacant_questions=None       #вопросы которые не в опросе
    selected_questions=None     #вопросы выбранные в опрос
    selected_poll=""            #выбранный опрос
    if not request.user.is_HR and not request.user.is_staff:
        return redirect("/")
    polls = Poll.objects.all()
    if poll_id != 0:
        selected_poll = Poll.objects.get(id=poll_id)
        selected_questions = PollAndQuestion.objects.filter(poll=selected_poll)
        if question_category == 1:
            vacant_questions = Question.objects.exclude(pollandquestion__poll=selected_poll).filter(many_answers=False).annotate(in_polls=Count("pollandquestion__id"))
        elif question_category == 2:
            vacant_questions = Question.objects.exclude(pollandquestion__poll=selected_poll).filter(many_answers=True).annotate(in_polls=Count("pollandquestion__id"))
        else:
            vacant_questions = Question.objects.exclude(pollandquestion__poll=selected_poll).annotate(in_polls=Count("pollandquestion__id"))
            
    if request.method == "POST":
        # Обработка удаления вопросов из опроса с которых сняли галочку в списке вопросов из выбранного опроса
        if request.POST.__contains__("question_remaind"):
            question_remaind = request.POST.getlist("question_remaind")
            for question in selected_questions:
                if str(question.id) not in question_remaind:
                    PollAndQuestion.objects.get(id=question.id).delete()
        else:
            # если сняли галочку с последнего вопроса, то удаляем все вопросы
            if selected_questions.count() >= 1:
                selected_questions.delete()

        # Добавляем в опрос вопросы на которые установили галочку из списка не добавленных вопросов вместе с баллами
        if request.POST.__contains__("question_append"):
            question_append = request.POST.getlist("question_append")
            for id, score in zip(request.POST.getlist("question_id"), request.POST.getlist("question_score")):
                if id in question_append:
                    question = Question.objects.get(id=id)
                    PollAndQuestion.objects.create(poll=selected_poll, question=question, score=score)                    

        selected_questions = PollAndQuestion.objects.filter(poll=selected_poll)
        if question_category == 1:
            vacant_questions = Question.objects.exclude(pollandquestion__poll=selected_poll).filter(many_answers=False).annotate(in_polls=Count("pollandquestion__id"))
        elif question_category == 2:
            vacant_questions = Question.objects.exclude(pollandquestion__poll=selected_poll).filter(many_answers=True).annotate(in_polls=Count("pollandquestion__id"))
        else:
            vacant_questions = Question.objects.exclude(pollandquestion__poll=selected_poll).annotate(in_polls=Count("pollandquestion__id"))
    return render(request, "question_choice_list.html", {
        "polls":polls,
        "poll_id":poll_id,
        "poll_title":selected_poll,
        "vacant_questions":vacant_questions,
        "selected_questions":selected_questions,
        "title":"Изменить опрос",
        "question_category":question_category,
        "button":"Сохранить"})

class UserCreate(CreateView):
    """
    Контроллер регистрации нового пользователя
    """
    model=User
    form_class=UserCreateForm
    template_name="user_create_update.html"
    success_url=reverse_lazy("main:users_management")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация нового пользователя"
        context["button"] = "Зарегистрировать"
        return context

class UserUpdate(LoginRequiredMixin, UpdateView):
    """
    Контроллер обновления данных пользователя
    """
    template_name="user_create_update.html"
    model=User
    form_class=UserUpdateForm
    success_url=reverse_lazy("main:users_management")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Изменить данные пользователя"
        context["button"] = "Обновить"
        return context

@login_required
def users_management(request):
    """
    Контроллер управления пользователями.
    Информация о всех зарегистрированных пользователях с возможностью выдачи права HR или удаления пользователя
    Функционал доступен авторизованному специалисту HR
    """
    if not request.user.is_HR and not request.user.is_staff:
        return redirect("/")
    if request.method == "POST":
        user_id = request.POST["user_id"]
        action = request.POST["action"]
        django_user = User.objects.get(id=user_id)
        permission = Permission.objects.get(name = "Can delete Пользователь")
        if action == "set_hr":
            django_user.is_HR = True
            django_user.user_permissions.add(permission)
            django_user.save()

        elif action == "unset_hr":
            django_user.is_HR = False
            django_user.user_permissions.remove(permission)
            django_user.save()

    users_list = User.objects.exclude(is_staff=True).order_by("id")
    all_questions_count = Question.objects.all().count()
    all_polls_count = Poll.objects.all().count()
    all_users_count = User.objects.exclude(is_staff = True).aggregate(users_count=Count("answered_user__user", distinct=True), total_score=Sum("answered_user__score"), total_polls=Count("answered_user__poll", distinct=True), total_questions=Count("answered_user__question_in_poll__question", distinct=True))
    return render(request, "users_management.html", {
        "title":"Перечень зарегистрированных пользователей",
        "users_list": users_list,
        "all_questions_count":all_questions_count,
        "all_polls_count":all_polls_count,
        "all_users_count":all_users_count
        })

@login_required
def user_delete(request, user_id):
    """
    Контроллер подтверждения удаления учетных записей пользователей
    """
    if not request.user.is_HR and not request.user.is_staff:
        return redirect("/")
    django_user = User.objects.get(id=user_id)
    if request.method == "POST":
        django_user.delete()
        return redirect(reverse_lazy("main:users_management"))
    return render(request, "user_confirm_delete.html", {
        "title":"Вы хотите удалить пользователя?",
        "django_user":django_user,
        "button":"Удалить"})

@login_required
def user_poll_choice(request):
    """
    Список опросов для выбора пользователем, выводится немного статистики по каждому опросу - сколько вопросов в опросе и на 
    сколько вопросов пользователь уже ответил. Контролируется дата публикации, до наступления которой опрос пройти нельзя.
    """
    polls_list=Poll.objects.filter(pub_date__lt=timezone.now()).annotate(question_count=Count("pollandquestion__id", distinct=True), question_answered=Count(Case(When(pollandquestion__question_in_poll__user=request.user, then=1))))
    return render(request, "user_poll_choice.html", {"title":"Выбор опроса","polls_list":polls_list})

@login_required
def user_survey(request, poll_id):
    """
    Контроллер формы опроса, передает вопросы по одному и записывает ответы пользователя.
    В случае, если пользователь уже отвечал на вопрос выводится его предыдущий ответ.
    """
    poll = Poll.objects.get(id=poll_id)
    paginator = Paginator(PollAndQuestion.objects.filter(poll=poll), 1)
    previous_user_answers = []    
    if request.method == "POST":
        if request.POST.__contains__("answer"):
            answers = request.POST.getlist("answer")
            question_in_poll = PollAndQuestion.objects.get(id=request.POST["question_id"])
            user_answer, _ = UserAnswer.objects.update_or_create(user=request.user, question_in_poll=question_in_poll)
            user_answer.answers.set(answers)
            user_answer.save()
            if request.POST["next_paginator_page"]:
                paginator_page = request.POST["next_paginator_page"] 
            else:
                return HttpResponseRedirect(reverse_lazy("main:user_poll_chioce"))
        else:
            paginator_page = request.POST["current_paginator_page"]
    else:
        paginator_page = 1

    page = paginator.get_page(paginator_page)

    #Выборка предыдущих ответов пользователя на вопрос, для отображения на каждом шаге опроса
    previous_user_answers_to_question = UserAnswer.objects.filter(user=request.user, question_in_poll=page.object_list[0])
    for previous_question_answers in previous_user_answers_to_question.all():
        for previous_answer in previous_question_answers.answers.all():
            previous_user_answers.append(previous_answer.id)

    return render(request, "user_survey.html", {"title":f"Вопрос {page.number} из {paginator.num_pages}", "page":page, "previous_user_answers":previous_user_answers})

@login_required
def user_statistic(request):
    current_user = User.objects.get(id=request.user.id)

    passed_questions_count = UserAnswer.objects.filter(user=current_user).count()
    passed_polls_count = Poll.objects.filter(useranswer__user=current_user).distinct().count()
    user_score = UserAnswer.objects.filter(user=current_user).aggregate(total_score=Sum("score"), min_score=Min("score"), max_score=Max("score"))

    import collections
    users_scores = collections.Counter()
    for answer in UserAnswer.objects.exclude(user__is_staff=True).exclude(user=current_user):
        users_scores[answer.user] += answer.score
    share = 100 / (len(users_scores) + 1)
    result = 0
    if not user_score["total_score"]:
        user_score["total_score"] = 0
    for _, score in users_scores.items():
        if score > user_score["total_score"]:
            result += share

    user_answers = {}
    for poll in Poll.objects.filter(useranswer__user=current_user).distinct().order_by("id"):
        user_questions = {}
        for question in UserAnswer.objects.filter(user=current_user).filter(poll=poll):
            answers_set = []
            for answer in question.answers.all():
                answers_set.append(answer.text)
            user_questions[question.question_in_poll.question.text] = answers_set
        user_answers[poll.title] = user_questions

    return render(request, "user_statistic.html", {
        "title":"Ваша статистика опросов",
        "answers_title":"Ваши ответы на вопросы",
        "passed_questions_count":passed_questions_count,
        "passed_polls_count":passed_polls_count,
        "score":user_score,
        "result":round(result),
        "user_answers":user_answers
        })

def hr_statistic(request, user_id):
    current_user = User.objects.get(id=user_id)
    passed_questions_count = UserAnswer.objects.filter(user=current_user).count()
    passed_polls_count = Poll.objects.filter(useranswer__user=current_user).distinct().count()
    user_score = UserAnswer.objects.filter(user=current_user).aggregate(total_score=Sum("score"), min_score=Min("score"), max_score=Max("score"))

    import collections
    users_scores = collections.Counter()
    for answer in UserAnswer.objects.exclude(user__is_staff=True).exclude(user=current_user):
        users_scores[answer.user] += answer.score
    share = 100 / (len(users_scores) + 1)
    result = 0
    if not user_score["total_score"]:
        user_score["total_score"] = 0
    for _, score in users_scores.items():
        if score > user_score["total_score"]:
            result += share

    user_answers = {}
    for poll in Poll.objects.filter(useranswer__user=current_user).distinct().order_by("id"):
        user_questions = {}
        for question in UserAnswer.objects.filter(user=current_user).filter(poll=poll):
            answers_set = []
            for answer in question.answers.all():
                answers_set.append(answer.text)
            user_questions[question.question_in_poll.question.text] = answers_set
        user_answers[poll.title] = user_questions

    if current_user.first_name:
        username = f"{current_user.first_name.capitalize()} {current_user.last_name.capitalize()}"
    else:
        username = current_user.username

    return render(request, "user_statistic.html", {
        "title":f"Cтатистика пользователя {username}",
        "answers_title":"Ответы пользователя",
        "passed_questions_count":passed_questions_count,
        "passed_polls_count":passed_polls_count,
        "score":user_score,
        "result":round(result),
        "user_answers":user_answers
        })