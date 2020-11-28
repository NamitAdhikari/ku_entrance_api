from django.urls import path, include

from . import views

urlpatterns = [
    path('create/', views.UserView.as_view()),
]