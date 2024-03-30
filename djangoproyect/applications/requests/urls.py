from django.urls import path

from applications.requests import views

urlpatterns = [
    path("", views.show_requests),
    path("change-status/<int:id>", views.change_status, name="change_status"),
    path("search/<str:query>", views.search, name="search"),
    path("<int:id>/", views.detail_request, name="request_detail"),
    path(
        "assign-request/<int:request_id>", views.assign_request, name="assign_request"
    ),
    path(
        "show-traceability/<int:request_id>",
        views.show_traceability,
        name="traceability",
    ),
    path("test-view/", views.test_view),
]
