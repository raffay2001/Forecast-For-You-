from django.urls import path
from . import views


app_name = 'application'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('login/', views.log_in, name = 'login'),
    path('signup/', views.signup, name = 'signup'),
    path('logout', views.log_out, name='logout')
]