"""dkango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from users.views import Login, Files, SpiderOperate,SpiderInfo,SpiderFile, SpiderStart, SpiderControl

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/login',Login.as_view()),
    path('files/post',Files.as_view()),
    path('spiders',SpiderOperate.as_view()),
    path('spider/<slug:id>',SpiderInfo.as_view()),
    path('spider/<slug:id>/dir',SpiderFile.as_view()),
    path('task/<slug:id>',SpiderStart.as_view()),
    path('task/control/<slug:id>/<int:flag>',SpiderControl.as_view())


]
