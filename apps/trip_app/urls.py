"""beltExam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^validation$',views.validation),
    url(r'^sendtosuccess$',views.success),
    url(r'^login$',views.login),
    url(r'^join/(?P<trip_id>\d+)$',views.join),
    url(r'^destination/(?P<trip_id>\d+)$',views.display),
    url(r'^addTrip$',views.addtrip),
    url(r'^add$',views.add),
    url(r'^logout$',views.logout),
    url(r'^home$',views.home)
]
