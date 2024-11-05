from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("timeline/", views.TimelineView.as_view()),
]