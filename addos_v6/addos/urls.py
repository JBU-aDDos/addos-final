from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),  # home 앱의 URL 포함
    path('user/', include('user.urls')),  # user 앱의 URL 포함
    path('mypage/', include('mypage.urls')),  # mypage 앱의 URL 포함
    path('', RedirectView.as_view(url='/home/index', permanent=True)),  # 루트 URL을 '/home/index'로 리디렉션
]