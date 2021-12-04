from django.urls import path
from employee.views import home


urlpatterns = [
    path('', home, name='employee_home'),
]
