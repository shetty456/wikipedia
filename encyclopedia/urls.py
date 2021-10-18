from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newpage", views.newpage, name="newpage"),
    path("change/<str:name>", views.change, name="change"),
    path("random",views.randomPage, name="random"),
    path("<str:name>", views.entry, name="entry")
]
