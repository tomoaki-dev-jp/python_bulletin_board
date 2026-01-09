from django.urls import path
from . import views

urlpatterns = [
    path("", views.board_list, name="board_list"),
    path("<slug:board_slug>/", views.thread_list, name="thread_list"),
    path("<slug:board_slug>/thread/<int:thread_id>/", views.thread_detail, name="thread_detail"),
    path("<slug:board_slug>/dat/<int:thread_id>.dat", views.dat_view, name="dat_view"),
]
