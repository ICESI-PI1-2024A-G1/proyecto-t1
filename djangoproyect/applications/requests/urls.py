from django.urls import path

from applications.requests import views


urlpatterns = [
    path("change-request/<int:id>", views.change_requests),
    path("search/<str:query>", views.search, name="search"),
    path("", views.show_requests),
    path("<int:id>/", views.detail_request, name="detail_request"),
]
