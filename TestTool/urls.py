"""TestTool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from testtools import views

urlpatterns = [
    path('index/', views.index),
    path('search_userinfo/', views.userinfo, name="verify_callback"),
    path('encrypt_str/', views.encrypt_str, name="encrypt_str"),
    path('decrypt_str/', views.decrypt_str, name="decrypt_str"),
#    path('audit_callback/', views.audit_callback),
#    path('lending_callback/', views.lending_callback),
#    path('repay_callback/', views.repay_callback),

]
