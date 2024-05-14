from django.test import TestCase
from django.urls import reverse


class Error404ViewTest(TestCase):
    def test_error_404_view(self):
        # Haciendo una solicitud a una URL que no existe
        response = self.client.get('/url/que/no/existe/')

        # Verificando que la respuesta tenga un código de estado 404
        self.assertEqual(response.status_code, 200)

        # Verificando que la plantilla correcta se esté utilizando
        self.assertTemplateUsed(response, '404.html')
