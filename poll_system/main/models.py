from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from os.path import splitext

def get_picture_path(instance, filename):
    return "%s%s"%(datetime.now().timestamp(),splitext(filename)[1])


class User(AbstractUser):
    is_HR = models.BooleanField("Специалист подразделения HR", default=False, help_text="Признак дает полномочия для добавления, редактирования и удаления вопросов, групп и опросов.")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Poll(models.Model):
    title = models.CharField("Название опроса", max_length=100, blank=False)
    description = models.TextField("Описание", blank=False)
    timer = models.PositiveSmallIntegerField("Ограничение времени для прохождения опроса в секундах (0 - без ограничения)", default=0)
    pub_date = models.DateTimeField("Дата публикации опроса", default=timezone.now)

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"

    def __str__(self):
        return self.title


class Question(models.Model):
    text = models.TextField("Текст вопроса", blank=False)
    many_answers = models.BooleanField("Для решения можно выбрать несколько ответов", default=False)
    timer = models.PositiveSmallIntegerField("Ограничение времени ответа в секундах (0 - без ограничения)", default=0)
    picture = models.ImageField("Картинка для этого вопроса", upload_to=get_picture_path, blank=True)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.CharField("Ответ", max_length=200, blank=True, null=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, verbose_name="Вопрос", related_name="answers")

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.text


class PollAndQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, verbose_name="Опрос")
    score = models.PositiveSmallIntegerField("Оценка за вопрос", default=0)

    class Meta:
        verbose_name = "Вопрос в опросе"
        verbose_name_plural = "Вопросы в опросах"

    def __str__(self):
        return f"{self.poll} - {self.question}"


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="answered_user")
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, verbose_name="Опрос")
    question_in_poll = models.ForeignKey(PollAndQuestion, on_delete=models.CASCADE, verbose_name="Вопрос в опросе", related_name="question_in_poll")
    score = models.PositiveSmallIntegerField("Оценка за вопрос", default=0)
    answers = models.ManyToManyField(Answer, blank=True, verbose_name="Ответы на вопрос")

    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователя"

    def __str__(self):
        return f"{self.user} - {self.question_in_poll.question.id}"

    def save(self, *args, **kwargs):
        self.poll = self.question_in_poll.poll
        self.score = self.question_in_poll.score
        super().save(*args, **kwargs)
