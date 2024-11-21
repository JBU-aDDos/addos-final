from django.urls import path
from . import views

app_name = 'mypage'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('traffic/', views.get_traffic_data, name='traffic'),
    path('suricata/', views.suricata, name='suricata'),
    # 다른 URL 패턴 추가
]