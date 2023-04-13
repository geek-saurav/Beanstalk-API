from django.urls import path
from . import views, authViews

urlpatterns=[
    path('test', views.test, name="test"),
    path('generate_api', views.generate_api, name="generate_api"),
    path('signup', authViews.signup, name="signup"),
    path('login', authViews.login, name="login")
]