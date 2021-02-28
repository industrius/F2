from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static
from django.conf import settings
from .views import Index, QuestionList, PollList, PollCreate, PollUpdate, QuestionDelete, PollDelete, PollDetail, QuestionDetail, question_choice_list, UserCreate, users_management, UserUpdate, user_delete, user_poll_choice, user_survey, question_create, question_update, user_statistic, hr_statistic

app_name = "main"
urlpatterns = [
    path("", Index.as_view(), name="index"),

    path("question_create/", question_create, name="question_create"),
    path("poll_create/", PollCreate.as_view(), name="poll_create"),

    path("question_update/<int:question_id>/", question_update, name="question_update"),
    path("poll_update/<int:pk>/", PollUpdate.as_view(), name="poll_update"),

    path("question_delete/<int:pk>/", QuestionDelete.as_view(), name="question_delete"),
    path("poll_delete/<int:pk>/", PollDelete.as_view(), name="poll_delete"),

    path("poll_detail/<int:pk>/", PollDetail.as_view(), name="poll_detail"),
    path("question_detail/<int:pk>/", QuestionDetail.as_view(), name="question_detail"),

    path("question_list/", QuestionList.as_view(), name="question_list"),
    path("poll_list/", PollList.as_view(), name="poll_list"),

    path("question_choice_list/<int:poll_id>/<int:question_category>/", question_choice_list, name="question_choice_list"),

    path("user_create/", UserCreate.as_view(), name="user_create"),
    path("user_update/<int:pk>/", UserUpdate.as_view(), name="user_update"),
    path("user_delete/<int:user_id>/", user_delete, name="user_delete"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("users_management/", users_management, name="users_management"),

    path("user_poll_chioce/", user_poll_choice, name="user_poll_chioce"),
    path("user_survey/<int:poll_id>/", user_survey, name="user_survey"),

    path("user_statistic/", user_statistic, name="user_statistic"),
    path("hr_statistic/<int:user_id>/", hr_statistic, name="hr_statistic")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)