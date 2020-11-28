from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('questions', views.QuestionView)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token),
    path('fetchquestion/', views.FetchNextQuestion.as_view()),
    path('startquiz/', views.StartQuiz.as_view()),
    path('payment/', views.PaymentVerify.as_view()),
]