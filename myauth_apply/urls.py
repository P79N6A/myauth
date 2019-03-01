"""myauth_apply URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth import urls as auth_urls
from . import view

urlpatterns = [
    url(r'^$',view.homepage),
    url(r'^hello$', view.hello),
    url(r'^login.html', view.login_mail),
    url(r'^main.html$',view.main_html),
    url(r'^mysqlaccoutinfo.html', view.apply_list),
    url(r'^mysqlaccoutinfo_add.html', view.apply_form),
    url(r'^face.html',view.face_action),
    url(r'^fuckadmin.html',view.fuckadmin),
    url(r'^fuckadmin_finish.html',view.fuckadmin_finish),
    url(r'^fuckadmin_bye.html',view.fuckadmin_bye)

]
