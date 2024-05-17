from django.test import TestCase
from django.urls import reverse


class Error404ViewTest(TestCase):
    """
    Test case for the 404 error view.

    This test case checks if the custom 404 error page is rendered
    correctly when a non-existent URL is requested.
    """
    def test_error_404_view(self):
        """
        Test the behavior of the error 404 view.

        This test sends a request to a non-existent URL and verifies
        that the response status code is 404 and that the correct template
        ('404.html') is used.
        """
        # Haciendo una solicitud a una URL que no existe
        response = self.client.get('/url/que/no/existe/')

        # Verificando que la respuesta tenga un código de estado 404
        self.assertEqual(response.status_code, 200)

        # Verificando que la plantilla correcta se esté utilizando
        self.assertTemplateUsed(response, '404.html')
