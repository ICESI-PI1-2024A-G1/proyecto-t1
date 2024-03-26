from django.urls import path
from . import views

app_name = 'permissions'

urlpatterns = [
    path("", views.permissions_view, name='permissions_view'),
    path("search/<str:query>", views.search, name="search"),
]