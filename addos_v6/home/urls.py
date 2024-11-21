from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('about/', views.send_email_view, name='about'),
]