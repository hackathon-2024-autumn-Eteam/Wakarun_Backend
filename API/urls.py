from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path('timeline/', views.TimelineView.as_view()),
    path('signin/', TokenObtainPairView.as_view(), name='signin'),
    path('signin/refresh/', TokenRefreshView.as_view(), name='signin_refresh'),
    path('signup/', views.RegisterView.as_view(), name='signup'),
    path('questions/', views.CreateQuestionView.as_view(), name='questions'),
    path('answers/', views.CreateAnswersView.as_view(), name='questions'),
    path('get-answer/', views.AnswersView.as_view(), name='get_answer'),
    ]