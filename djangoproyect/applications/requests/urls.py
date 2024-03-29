from django.urls import path

from applications.requests import views

urlpatterns = [
    path("change-status/<int:id>", views.change_status),
    path("search/<str:query>", views.search, name="search"),
    path("", views.show_requests),
    path("<int:id>/", views.detail_request, name="request_detail"),
    path("assign-request/<int:request_id>", views.assign_request),
    path(
        "show-traceability/<int:request_id>",
        views.show_traceability,
        name="traceability",
    ),
]
