from django.shortcuts import render


def error_404_view(request, exception):
    """
    View function for handling 404 errors.

    Args:
        request (HttpRequest): The HTTP request object.
        exception: The exception that triggered the 404 error.

    Returns:
        HttpResponse: Rendered response for the 404 error page.
    """
    return render(request, "404.html")
