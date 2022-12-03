from django.urls import path

from . import views


app_name = 'resume'

urlpatterns = [
    path("", views.index, name="index"),
    path("message", views.send_message, name='message'),
]
