from django.urls import include, re_path, path
from .views import polls_list, polls_detail

urlpatterns = [
    path('', include('polls.urls')),
    path("polls/", polls_list, name="polls_list"),
    path("polls/<int:pk>/", polls_detail, name="polls_detail")
]
