from django.test import TestCase
from apps.forms.models import Country
from django.utils import timezone
from unittest.mock import patch
from apps.forms.models import City, Bank, AccountType, Dependency, CostCenter
from .views import get_cities_with_countries, get_bank_data, get_account_types, get_dependence_data, get_cost_center_data
from django.test import TestCase, RequestFactory
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from .views import show_requests, change_status
from datetime import timedelta
from django.test import TestCase, RequestFactory
from unittest.mock import patch, MagicMock
from django.contrib.messages import get_messages
from utils.models import CustomUser
from unittest import mock
from django.test import TestCase
from unittest.mock import patch, MagicMock
from .views import *
from apps.forms.models import TravelAdvanceRequest, AdvanceLegalization, BillingAccount, Requisition, TravelExpenseLegalization
from django.http import Http404

class TestViews(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_superuser(username='testuser', email="testmail@hotmail.com", password='12345')

    @patch('apps.forms.models.City.objects.select_related')
    def test_get_cities_with_countries(self, mock_objects):
        country = Country(name='Colombia', code='CO')
        mock_objects.return_value.order_by.return_value.all.return_value = [
            City(id=1, name='Bogota', country=country)
        ]
        result = get_cities_with_countries()
        self.assertEqual(result, [{'city_id': 1, 'city_name': 'Bogota', 'country_name': 'Colombia', 'country_code': 'CO'}])

    @patch('apps.forms.models.Bank.objects')
    def test_get_bank_data(self, mock_objects):
        mock_objects.all.return_value = [Bank(id=1, name='Bank of America')]
        result = get_bank_data()
        self.assertEqual(result, [{'bank_id': 1, 'bank_name': 'Bank of America'}])

    @patch('apps.forms.models.AccountType.objects')
    def test_get_account_types(self, mock_objects):
        mock_objects.all.return_value = [AccountType(id=1, name='Savings')]
        result = get_account_types()
        self.assertEqual(result, [{'account_type_id': 1, 'account_type_name': 'Savings'}])

    @patch('apps.forms.models.Dependency.objects')
    def test_get_dependence_data(self, mock_objects):
        mock_objects.all.return_value = [Dependency(id=1, name='Dependence 1')]
        result = get_dependence_data()
        self.assertEqual(result, [{'dependence_id': 1, 'dependence_name': 'Dependence 1'}])

    @patch('apps.forms.models.CostCenter.objects')
    def test_get_cost_center_data(self, mock_objects):
        mock_objects.all.return_value = [CostCenter(id=1, name='Cost Center 1')]
        result = get_cost_center_data()
        self.assertEqual(result, [{'cost_center_id': 1, 'cost_center_name': 'Cost Center 1'}])

    @patch('apps.internalRequests.views.get_all_requests')
    @patch('apps.internalRequests.views.Team.objects.filter')
    def test_show_requests(self, mock_filter, mock_get_all_requests):
        request = self.factory.get('/requests/')
        request.user = AnonymousUser()
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        mock_filter.return_value.exists.return_value = False
        mock_get_all_requests.return_value = []

        response = show_requests(request)

        self.assertEqual(response.status_code, 302)

    @patch('apps.internalRequests.views.get_all_requests')
    @patch('apps.internalRequests.views.Team.objects.filter')
    
    def test_show_requests_with_messages(self, mock_filter, mock_get_all_requests):
        request = self.factory.get('/requests/?changeStatusDone=true')
        request.user = AnonymousUser()
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        mock_filter.return_value.exists.return_value = False
        mock_get_all_requests.return_value = []

        response = show_requests(request)

        self.assertEqual(response.status_code, 302) 
        self.assertFalse('El estado de la solicitud ha sido actualizado correctamente.' in [str(m) for m in messages])

    @patch('apps.internalRequests.views.get_all_requests')
    @patch('apps.internalRequests.views.Team.objects.filter')
    @patch('apps.internalRequests.views.Team.objects.get')
    def test_show_requests_as_leader(self, mock_get, mock_filter, mock_get_all_requests):
        request = self.factory.get('/requests/')
        request.user = CustomUser(is_leader=True)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        mock_filter.return_value.exists.return_value = True
        mock_get.return_value.typeForm = 'formType'
        mock_request = MagicMock()
        mock_request.document = 'formType'
        mock_request.status = 'PENDIENTE'  # Set a return value for mock.status
        mock_get_all_requests.return_value = [mock_request]

        response = show_requests(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'requests', response.content)
    
    @patch('apps.internalRequests.views.get_all_requests')
    def test_show_requests_as_member(self, mock_get_all_requests):
        request = self.factory.get('/requests/')
        request.user = CustomUser(is_member=True)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        mock_request = MagicMock()
        mock_request.member.id = request.user.id
        mock_request.status = 'PENDIENTE'  # Set a return value for mock.status
        mock_get_all_requests.return_value = [mock_request]

        response = show_requests(request)

    @patch('apps.internalRequests.views.get_all_requests')
    def test_show_requests_as_applicant(self, mock_get_all_requests):
        request = self.factory.get('/requests/')
        request.user = CustomUser(is_applicant=True)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        mock_request = MagicMock()
        mock_request.id_person = request.user.id
        mock_get_all_requests.return_value = [mock_request]

        response = show_requests(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'requests', response.content)

    @patch('apps.internalRequests.views.get_request_by_id')
    def test_change_status_get(self, mock_get_request_by_id):
        request = self.factory.get('/change_status/1/')
        request.user = CustomUser()
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        mock_request = MagicMock()
        mock_request.status = 'PENDIENTE'
        mock_get_request_by_id.return_value = mock_request

        response = change_status(request, 1)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'changeStatus', response.content)

    @patch('apps.internalRequests.views.get_request_by_id')
    def test_change_status_post(self, mock_get_request_by_id):
        request = self.factory.post('/change_status/1/', {'newStatus': 'EN REVISIÓN', 'reason': 'Just because'})
        request.user = CustomUser()
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        mock_request = MagicMock()
        mock_request.status = 'PENDIENTE'
        mock_get_request_by_id.return_value = mock_request

        response = change_status(request, 1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_request.status, 'EN REVISIÓN')

    @patch('apps.internalRequests.views.get_request_by_id')
    def test_change_status_get_pending(self, mock_get_request_by_id):
        request = self.factory.get('/change_status/1/')
        request.user = CustomUser()
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        mock_request = MagicMock()
        mock_request.status = 'PENDIENTE'
        mock_get_request_by_id.return_value = mock_request

        response = change_status(request, 1)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'changeStatus', response.content)

    @patch('apps.internalRequests.views.get_request_by_id')
    def test_change_status_get_for_approval(self, mock_get_request_by_id):
        request = self.factory.get('/change_status/1/')
        request.user = CustomUser()
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        mock_request = MagicMock()
        mock_request.status = 'POR APROBAR'
        mock_get_request_by_id.return_value = mock_request

        response = change_status(request, 1)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'changeStatus', response.content)

    @patch('apps.internalRequests.views.get_request_by_id')
    @patch('apps.internalRequests.views.Traceability.objects.create')
    def test_change_status_post(self, mock_traceability_create, mock_get_request_by_id):
        request = self.factory.post('/change_status/1/', {'newStatus': 'EN REVISIÓN', 'reason': 'Just because'})
        request.user = CustomUser(id='1')
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        mock_request = MagicMock()
        mock_request.status = 'PENDIENTE'
        mock_get_request_by_id.return_value = mock_request

        mock_traceability = MagicMock()
        mock_traceability_create.return_value = mock_traceability

        response = change_status(request, 1)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(mock_request.status, 'EN REVISIÓN')


    @patch('apps.internalRequests.views.get_request_by_id')
    def test_change_status_post_exception(self, mock_get_request_by_id):
        request = self.factory.post('/change_status/1/', {'newStatus': 'EN REVISIÓN', 'reason': 'Just because'})
        request.user = CustomUser()
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        mock_request = MagicMock()
        mock_request.status = 'PENDIENTE'
        mock_request.save.side_effect = Exception('Test exception')
        mock_get_request_by_id.return_value = mock_request

        response = change_status(request, 1)

        self.assertEqual(response.status_code, 500)

    @patch.object(TravelAdvanceRequest.objects, 'get', MagicMock(side_effect=TravelAdvanceRequest.DoesNotExist))
    @patch.object(AdvanceLegalization.objects, 'get', MagicMock(side_effect=AdvanceLegalization.DoesNotExist))
    @patch.object(BillingAccount.objects, 'get', MagicMock(side_effect=BillingAccount.DoesNotExist))
    @patch.object(Requisition.objects, 'get', MagicMock(side_effect=Requisition.DoesNotExist))
    @patch.object(TravelExpenseLegalization.objects, 'get', MagicMock(return_value='Found'))
    def test_get_request_by_id_found(self):
        result = get_request_by_id(1)
        self.assertEqual(result, 'Found')

    @patch.object(TravelAdvanceRequest.objects, 'get', MagicMock(side_effect=TravelAdvanceRequest.DoesNotExist))
    @patch.object(AdvanceLegalization.objects, 'get', MagicMock(side_effect=AdvanceLegalization.DoesNotExist))
    @patch.object(BillingAccount.objects, 'get', MagicMock(side_effect=BillingAccount.DoesNotExist))
    @patch.object(Requisition.objects, 'get', MagicMock(side_effect=Requisition.DoesNotExist))
    @patch.object(TravelExpenseLegalization.objects, 'get', MagicMock(side_effect=TravelExpenseLegalization.DoesNotExist))
    def test_get_request_by_id_not_found(self):
        with self.assertRaises(Http404):
            get_request_by_id(1)

    @patch.object(TravelAdvanceRequest.objects, 'all', MagicMock(return_value=[]))
    @patch.object(AdvanceLegalization.objects, 'all', MagicMock(return_value=[]))
    @patch.object(BillingAccount.objects, 'all', MagicMock(return_value=[]))
    @patch.object(Requisition.objects, 'all', MagicMock(return_value=[]))
    @patch.object(TravelExpenseLegalization.objects, 'all', MagicMock(return_value=[]))
    def test_get_all_requests_no_form_type(self):
        result = get_all_requests()
        self.assertEqual(result, [])

    @patch.object(TravelAdvanceRequest.objects, 'all', MagicMock(return_value=[]))
    @patch.object(AdvanceLegalization.objects, 'all', MagicMock(return_value=[]))
    @patch.object(BillingAccount.objects, 'all', MagicMock(return_value=[]))
    @patch.object(Requisition.objects, 'all', MagicMock(return_value=[]))
    @patch.object(TravelExpenseLegalization.objects, 'all', MagicMock(return_value=[]))
    def test_get_all_requests_with_form_type(self):
        result = get_all_requests('TravelExpenseLegalization')
        self.assertEqual(result, [])

    @patch('apps.internalRequests.views.get_all_requests')
    def test_show_requests_change_status_done(self,  mock_get_all_requests):
        request = self.factory.get('/requests/?changeStatusDone=true')
        request.user = CustomUser()
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        mock_request = MagicMock()
        mock_request.id_person = request.user.id
        mock_request.status = "POR APROBAR"
        mock_get_all_requests.return_value = [mock_request]
        response = show_requests(request)

        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertTrue('El estado de la solicitud ha sido actualizado correctamente.' in [str(m) for m in messages])
    @patch('apps.internalRequests.views.get_all_requests')
    def test_show_requests_change_status_failed(self,  mock_get_all_requests):
        request = self.factory.get('/requests/?changeStatusFailed=true')
        request.user = CustomUser()
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        mock_request = MagicMock()
        mock_request.id_person = request.user.id
        mock_request.status = "POR APROBAR"
        mock_get_all_requests.return_value = [mock_request]
        response = show_requests(request)

        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertTrue('No se pudo realizar la operación.' in [str(m) for m in messages])

    @patch('apps.internalRequests.views.get_all_requests')
    def test_show_requests_review_done(self,  mock_get_all_requests):
        request = self.factory.get('/requests/?reviewDone=true')
        request.user = CustomUser()
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = show_requests(request)
        mock_request = MagicMock()
        mock_request.status = "POR APROBAR"
        mock_request.id_person = request.user.id
        mock_get_all_requests.return_value = [mock_request]
        response = show_requests(request)

        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertTrue('El formulario ha sido revisado.' in [str(m) for m in messages])
    @patch('apps.internalRequests.views.get_all_requests')
    def test_show_requests_fix_request_done(self,  mock_get_all_requests):
        request = self.factory.get('/requests/?fixRequestDone=true')
        request.user = CustomUser()
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        mock_request = MagicMock()
        mock_request.status = "POR APROBAR"
        mock_request.id_person = request.user.id
        mock_get_all_requests.return_value = [mock_request]
        response = show_requests(request)

        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertTrue('El formulario ha sido enviado para revisión.' in [str(m) for m in messages])

    @patch('apps.internalRequests.views.get_all_requests')
    def test_show_requests_fix_request_failed(self, mock_get_all_requests):
        request = self.factory.get('/requests/?fixRequestFailed=true')
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        mock_request = MagicMock()
        mock_request.status = "POR APROBAR"
        mock_request.id_person = request.user.id
        mock_get_all_requests.return_value = [mock_request]
        response = show_requests(request)

        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertTrue('No se pudo enviar el formulario para revisión.' in [str(m) for m in messages])
    @patch('apps.internalRequests.views.get_all_requests')
    def test_show_requests_change_final_date_done(self,  mock_get_all_requests):
        request = self.factory.get('/requests/?changeFinalDateDone=true')
        request.user = CustomUser()
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        mock_request = MagicMock()
        mock_request.status = "POR APROBAR"
        mock_request.id_person = request.user.id
        mock_get_all_requests.return_value = [mock_request]
        response = show_requests(request)

        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertTrue('La fecha final de la solicitud ha sido actualizada correctamente.' in [str(m) for m in messages])

    @patch('apps.internalRequests.views.get_all_requests')
    def test_show_requests_change_final_date_failed(self,  mock_get_all_requests):
        request = self.factory.get('/requests/?changeFinalDateFailed=true')
        request.user = CustomUser()
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        mock_request = MagicMock()
        mock_request.status = "POR APROBAR"
        mock_request.id_person = request.user.id
        mock_get_all_requests.return_value = [mock_request]
        response = show_requests(request)

        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertTrue('No se pudo actualizar la fecha final de la solicitud.' in [str(m) for m in messages])

    @patch.object(Team.objects, 'filter', MagicMock(return_value=MagicMock(exists=MagicMock(return_value=False))))
    @patch('apps.internalRequests.views.get_all_requests')
    def test_show_requests_leader_no_team(self,  mock_get_all_requests):
        request = self.factory.get('/requests/')
        request.user = CustomUser(id='1', is_leader=True)
        messages = get_messages(request)
        mock_request = MagicMock()
        mock_request.status = "POR APROBAR"
        mock_request.id_person = request.user.id
        mock_get_all_requests.return_value = [mock_request]
        response = show_requests(request)

        self.assertEqual(response.status_code, 200)  # Expecting a successful response
        self.assertIn(b'internalRequests', response.content)

    @patch('apps.internalRequests.views.get_request_by_id')
    @patch('apps.internalRequests.views.utils.send_verification_email')
    def test_change_status_post_superuser(self, mock_send_verification_email, mock_get_request_by_id):
        request = self.factory.post('/change_status/1/', {'newStatus': 'EN REVISIÓN', 'reason': 'Just because'})
        request.user = self.user  # Use the User object you created earlier
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        mock_request = MagicMock()
        mock_request.status = 'PENDIENTE'
        mock_request.team_id = Team(leader=CustomUser(id='2'))
        mock_get_request_by_id.return_value = mock_request

        response = change_status(request, 1)
        self.assertEqual(response.status_code, 500)

    @patch('apps.internalRequests.views.get_request_by_id')
    def test_change_status_post_advance_legalization(self, mock_get_request_by_id):
        request = self.factory.post('/change-status/1', {'newStatus': 'POR APROBAR', 'reason': 'test reason'})
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        # Create a mock request
        mock_request = MagicMock(id= 1, spec=AdvanceLegalization)
    
        mock_request.status = "EN REVISIÓN"
        mock_request.__class__ = AdvanceLegalization
        mock_get_request_by_id.return_value = mock_request


        response = change_status(request, 1)
        self.assertEqual(response.status_code, 500)

    @patch('apps.internalRequests.views.get_request_by_id')
    def tesst_change_status_billing_account(self, mock_get_request_by_id):
        request = self.factory.post('/change_status/1')
        request.user = self.user

        # Create a mock request
        mock_request = MagicMock(id= 1, spec=BillingAccount)
        mock_request.status = "POR APROBAR"
        mock_get_request_by_id.return_value = mock_request

        response = change_status(request, 1)
        self.assertEqual(response.status_code, 500)
        mock_get_request_by_id.assert_called_once_with(1)
