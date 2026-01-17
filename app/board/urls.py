from django.urls import path
from . import views
from . import api

urlpatterns = [
    path("", views.board_list, name="board_list"),
    path("<slug:board_slug>/", views.thread_list, name="thread_list"),
    path("<slug:board_slug>/thread/<int:thread_id>/", views.thread_detail, name="thread_detail"),
    path("<slug:board_slug>/dat/<int:thread_id>.dat", views.dat_view, name="dat_view"),

    # API
    path("api/<slug:board_slug>/threads/", api.thread_list_api, name="api_thread_list"),
    path("api/<slug:board_slug>/thread/<int:thread_id>/", api.thread_detail_api, name="api_thread_detail"),
    path("api/<slug:board_slug>/thread/<int:thread_id>/posts/", api.post_create_api, name="api_post_create"),

]
