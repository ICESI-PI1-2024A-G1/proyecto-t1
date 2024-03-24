from django.urls import reverse

# Middleware to reset the has_registered session variable

class ResetHasRegisteredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.path != reverse('registration:verifyEmail_view'):
            request.session['has_registered'] = False
        else:
            request.session['has_registered'] = True

        return response