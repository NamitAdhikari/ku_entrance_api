from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('login/', obtain_auth_token),
    path('fetchquestion/', views.FetchNextQuestion.as_view()),
    path('startquiz/', views.StartQuiz.as_view()),
    path('payment/', views.PaymentVerify.as_view()),
    path('subject/', views.Subject.as_view()),
]