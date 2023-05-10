from django.urls import path
from . import views

urlpatterns = [
    path('register', views.RegisterUser.as_view()),
    path("tasks/", views.TaskView.as_view()),
    path("tasks/<int:pk>", views.SingleTaskView.as_view()),
    path("tasks/complete", views.complete_task)

]
