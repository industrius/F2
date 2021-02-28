from django.contrib import admin
from .models import Question, Poll, PollAndQuestion, User, UserAnswer

admin.site.register(User)
admin.site.register(Question)
admin.site.register(Poll)
admin.site.register(PollAndQuestion)
admin.site.register(UserAnswer)