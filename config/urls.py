"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from recipe import views

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('recipe/', include('recipe.urls')),
    # path('mypage/', include('mypageapp.urls'))
=======
    path('mypage/', include('mypageapp.urls')),
    path('users/', include('users.urls')),#yeon
    
>>>>>>> 7bdbe9d0091871d047a5c6458de1d8c5f50f2534
]
