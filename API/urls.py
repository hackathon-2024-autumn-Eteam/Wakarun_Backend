from django.urls import path

from . import views

urlpatterns = [
    path("timeline/", views.TimelineView.as_view()),
]