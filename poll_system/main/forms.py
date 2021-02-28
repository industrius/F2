from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Question, Poll, User, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"
        widgets = {
            "picture":forms.widgets.ClearableFileInput(attrs={"multiple":False})
        }

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = "__all__"

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ("text",)
