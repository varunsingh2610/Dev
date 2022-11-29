from django.urls import path
from .views import *


urlpatterns = [
    path('movies', IndexView.as_view(), name='index'),
]
