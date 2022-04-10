from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name="index"),
    path('add_book', views.BookAdd.as_view(), name="add_book")
]
