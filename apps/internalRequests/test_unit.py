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
from apps.teams.models import Team

class TestViews(TestCase): #pragma: no cover

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
        real_user = CustomUser.objects.create_user(
        username='testuser', email='test@example.com', password='testpassword')
        mock_request.team_id.leader = real_user  # Return the real CustomUser
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
        real_user = CustomUser.objects.create_user(
        username='testuser', email='test@example.com', password='testpassword')
        mock_request.team_id.leader = real_user  # Return the real CustomUser
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
        real_user = CustomUser.objects.create_user(
        username='testuser', email='test@example.com', password='testpassword')
        mock_request.team_id.leader = real_user  # Return the real CustomUser
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
        real_user = CustomUser.objects.create_user(
        username='testuser', email='test@example.com', password='testpassword')
        mock_request.team_id.leader = real_user  # Return the real CustomUser
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
        real_user = CustomUser.objects.create_user(
        username='testuser', email='test@example.com', password='testpassword')
        mock_request.team_id.leader = real_user  # Return the real CustomUser

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
        real_user = CustomUser.objects.create_user(
        username='testuser', email='test@example.com', password='testpassword')
        mock_request.team_id.leader = real_user  # Return the real CustomUser
        mock_get_all_requests.return_value = [mock_request]
        response = show_requests(request)

        self.assertEqual(response.status_code, 200) 
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

        # Create a real CustomUser
        real_user = CustomUser.objects.create_user(
        username='testuser', email='test@example.com', password='testpassword')
        # Create a mock request
    
        mock_request = MagicMock(id= 1, spec=AdvanceLegalization)
    
        mock_request.status = "EN REVISIÓN"
        mock_request.__class__ = AdvanceLegalization
        mock_request.team_id.leader = real_user  # Return the real CustomUser
        mock_get_request_by_id.return_value = mock_request

        response = change_status(request, 1)
        self.assertEqual(response.status_code, 500)

    @patch('apps.internalRequests.views.get_request_by_id')
    def test_change_status_post_billing_account(self, mock_get_request_by_id):
        request = self.factory.post('/change-status/1', {'newStatus': 'POR APROBAR', 'reason': 'test reason'})
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        # Create a real CustomUser
        real_user = CustomUser.objects.create_user(
        username='testuser', email='test@example.com', password='testpassword')
        # Create a mock request
    
        mock_request = MagicMock(id= 1, spec=BillingAccount)
    
        mock_request.status = "EN REVISIÓN"
        mock_request.__class__ = BillingAccount
        mock_request.team_id.leader = real_user  # Return the real CustomUser
        mock_get_request_by_id.return_value = mock_request

        response = change_status(request, 1)
        self.assertEqual(response.status_code, 500)

    @patch('apps.internalRequests.views.get_request_by_id')
    def test_change_status_post_requisition(self, mock_get_request_by_id):
        request = self.factory.post('/change-status/1', {'newStatus': 'POR APROBAR', 'reason': 'test reason'})
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        # Create a real CustomUser
        real_user = CustomUser.objects.create_user(
        username='testuser', email='test@example.com', password='testpassword')
        # Create a mock request
    
        mock_request = MagicMock(id= 1, spec=Requisition)
    
        mock_request.status = "EN REVISIÓN"
        mock_request.__class__ = Requisition
        mock_request.team_id.leader = real_user  # Return the real CustomUser
        mock_get_request_by_id.return_value = mock_request

        response = change_status(request, 1)
        self.assertEqual(response.status_code, 500)

    @patch('apps.internalRequests.views.get_request_by_id')
    def test_change_status_post_travel_advance_request(self, mock_get_request_by_id):
        request = self.factory.post('/change-status/1', {'newStatus': 'POR APROBAR', 'reason': 'test reason'})
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        # Create a real CustomUser
        real_user = CustomUser.objects.create_user(
        username='testuser', email='test@example.com', password='testpassword')
        # Create a mock request
    
        mock_request = MagicMock(id= 1, spec=TravelAdvanceRequest)
    
        mock_request.status = "EN REVISIÓN"
        mock_request.__class__ = TravelAdvanceRequest
        mock_request.team_id.leader = real_user  # Return the real CustomUser
        mock_get_request_by_id.return_value = mock_request

        response = change_status(request, 1)
        self.assertEqual(response.status_code, 500)
        
    @patch('apps.teams.models.Team.objects.all')
    @patch('apps.internalRequests.views.get_request_by_id')
    def test_change_status_post_travel_expense_legalization(self, mock_get_request_by_id, mock_team_all):
        request = self.factory.post('/change-status/1', {'newStatus': 'POR APROBAR', 'reason': 'test reason'})
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        # Create a real CustomUser
        real_user = CustomUser.objects.create_user(
        username='testuser', email='test@example.com', password='testpassword')
        # Create a mock request
        real_team = Team.objects.create(id=1, name='Test Team', leader=real_user)
        real_team.save()
        id_person_user = CustomUser.objects.create_user(
        username='id_person_user', email='id_person@example.com', password='testpassword')
        member = CustomUser.objects.create_user(
        username='id_memer', email='id_person@example.com', password='testpassword', is_member=True)
        # Configure the mock to return a list containing the mock Team when called
        mock_team_all.return_value = [real_team]
  
        mock_request = MagicMock(id= 1, spec=TravelExpenseLegalization)
        mock_request.member = member
        mock_request.id_person = id_person_user.id
        mock_request.status = "EN REVISIÓN"
        mock_request.__class__ = TravelExpenseLegalization
        mock_request.team_id = real_team
        mock_request.team_id.id = real_team.id
        mock_request.fullname = "ernesto"
        mock_request.cost_center = "010202"
        mock_request.bank = "Bancolombia"
        mock_request.account_type = "Ahorros"
        mock_request.team_id.leader = real_user  
        mock_get_request_by_id.return_value = mock_request

        response = change_status(request, 1)
        self.assertEqual(response.status_code, 200)

    @patch('apps.internalRequests.views.get_request_by_id')
    def test_change_status_post_no(self, mock_get_request_by_id):
        request = self.factory.post('/change-status/1', {'newStatus': 'POR APROBAR', 'reason': 'test reason'})
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        # Configure the mock to return a list containing the mock Team when called
        # Create a real CustomUser
        real_user = CustomUser.objects.create_user(
        username='testuser', email='test@example.com', password='testpassword')
        # Create a mock request
        # Create a real Team
        # Configure the mock to return a list containing the mock Team when called
        mock_request = MagicMock(id= 1)

        mock_request.status = "EN REVISIÓN"
        mock_request.team_id = 1# Return the real Team
        mock_get_request_by_id.return_value = mock_request

        response = change_status(request, 1)
        self.assertEqual(response.status_code, 500)

    @patch('apps.internalRequests.views.get_request_by_id')
    def test_change_final_date_get(self, mock_get_request_by_id):
        request = self.factory.get('/change_final_date/1')
        request.user = self.user

        # Create a mock request
        mock_request = MagicMock(spec=TravelAdvanceRequest)
        mock_request.final_date.strftime.return_value = '2022-12-31'
        mock_get_request_by_id.return_value = mock_request

        response = change_final_date(request, 1)
        self.assertEqual(response.status_code, 200)
        mock_get_request_by_id.assert_called_once_with(1)

    @patch('apps.internalRequests.views.get_request_by_id')
    def test_change_final_date_post(self, mock_get_request_by_id):
        request = self.factory.post('/change_final_date/1', {'newFinalDate': '2023-01-01', 'reason': 'test reason'})
        request.user = self.user

        # Create a mock request
        mock_request = MagicMock(spec=TravelAdvanceRequest)
        mock_request.status = 'EN REVISIÓN'
        mock_request.final_date.strftime.return_value = '2022-12-31'
        mock_get_request_by_id.return_value = mock_request

        response = change_final_date(request, 1)
        self.assertEqual(response.status_code, 500)
        mock_get_request_by_id.assert_called_once_with(1)

    @patch('apps.internalRequests.views.get_request_by_id')
    @patch('apps.teams.models.Team.objects.get')
    def test_detail_request_post_save_to_file(self, mock_team_get, mock_get_request_by_id):
        request = self.factory.post('/detail_request/1', {'pdf': 'True', 'save_to_file': 'True', 'trace': 'False'})
        request.user = self.user

        # Create a real CustomUser for the team leader
        real_user = User.objects.create_user(
            username='leader', email='leader@example.com', password='testpassword')

        # Create a real Team
        real_team = Team.objects.create(name='Test Team', leader=real_user)
        mock_json = '{"expense1": 100, "expense2": 200}'
        # Create a mock request
        mock_request = MagicMock(spec=TravelAdvanceRequest)
        mock_request.status = "EN REVISIÓN"
        mock_request.team_id = real_team  # Return the real Team
        mock_request.expenses = mock_json
        mock_get_request_by_id.return_value = mock_request

        # Configure the mock to return the real Team when called
        mock_team_get.return_value = real_team

        response = detail_request(request, 1, pdf=True, save_to_file=True, trace=False)
        self.assertEqual(response.status_code, 200)
        mock_get_request_by_id.assert_called_once_with(1)

    @patch('apps.internalRequests.views.get_request_by_id')
    @patch('apps.teams.models.Team.objects.get')
    def test_request_detail(self, mock_team_get, mock_get_request_by_id):
        request = self.factory.post('/detail_request/1', {'pdf': 'True', 'save_to_file': 'True', 'trace': 'True'})
        request.user = self.user

        # Crear un usuario real para el líder del equipo
        real_user = User.objects.create_user(
            username='leader', email='leader@example.com', password='testpassword', )

        real_team = Team.objects.create(name='Test Team', leader=real_user, typeForm="Requisición")
        real_team.save()
        mock_json = '{"expense1": 100, "expense2": 200}'
        # Create a mock request
        mock_request = MagicMock(spec=Requisition)
        mock_request.status = "EN REVISIÓN"
        mock_request.expenses = mock_json
        mock_request.team_id = real_team  # Devolver el equipo real
        mock_request.pdf_file.url = "/path/to/pdf"  # Ruta ficticia al archivo PDF
        mock_get_request_by_id.return_value = mock_request

        # Configurar el mock para devolver el equipo real cuando se llame
        mock_team_get.return_value = real_team

        response = detail_request(request, 1, pdf=True, save_to_file=True, trace=True)
        self.assertEqual(response.status_code, 200)

    def test_show_traceability(self):
            # Crear una trazabilidad ficticia
            Traceability.objects.create(request=1, date=timezone.now(), modified_by_id=self.user.id, prev_state="EN REVISIÓN", new_state="DEVUELTO")

            request = self.factory.get('/show_traceability/1')
            request.user = self.user

            response = show_traceability(request, 1)
            self.assertEqual(response.status_code, 200)

    def test_assign_request_post(self):
        # Crear una solicitud ficticia
        mock_request = TravelAdvanceRequest.objects.create(member=self.user, request_date=timezone.now(), departure_date=timezone.now(), return_date=timezone.now() + timedelta(days=7))
        
        # Crear un equipo ficticio
        mock_team = Team.objects.create(name='Test Team', leader=self.user)
        mock_team.save()
        mock_request.team_id = mock_team
        mock_request.team_id.leader = mock_team.leader
        request = self.factory.post('/assign_request/1', {'user_id': self.user.id})
        request.user = self.user

        response = assign_request(request, mock_request.id)
        self.assertEqual(response.status_code, 302)  # Redirección después de la asignación

        # Verificar que la solicitud fue asignada al usuario
        mock_request.refresh_from_db()
        self.assertEqual(mock_request.member, self.user)

    @patch('apps.internalRequests.views.get_request_by_id')
    def test_assign_request_get(self, mock_get_request_by_id):
        # Crear una solicitud ficticia
        mock_request = TravelAdvanceRequest.objects.create(member=self.user, request_date=timezone.now(), departure_date=timezone.now(), return_date=timezone.now() + timedelta(days=7))

        # Crear un equipo ficticio
        mock_team = Team.objects.create(name='Test Team', leader=self.user)
        mock_request = MagicMock(id= 1, spec=TravelExpenseLegalization)
        mock_request.status = "EN REVISIÓN"
        mock_request.__class__ = TravelExpenseLegalization
        mock_request.fullname = "ernesto"
        mock_request.cost_center = "010202"
        mock_request.bank = "Bancolombia"
        mock_request.account_type = "Ahorros" 
        mock_get_request_by_id.return_value = mock_request

        request = self.factory.get('/assign_request/1')
        request.user = self.user

        response = assign_request(request, mock_request.id)
        self.assertEqual(response.status_code, 200)  # Debería renderizar la página correctamente
        
    @patch('apps.internalRequests.views.get_request_by_id')
    def test_assign_request_get_Adv(self, mock_get_request_by_id):
        # Crear una solicitud ficticia
        mock_request = AdvanceLegalization.objects.create(
            member=self.user, request_date=timezone.now(),
              total=2, advance_total=2,  employee_balance_value= 
              2,icesi_balance_value=2, 
              signature_status=True,
                dependence = "8465",
                cost_center = "010202",
                purchase_reason = "lol",
                bank = "Bancolombia",
                account_type = "Ahorros",
                account_number = "5851645"
              )

        # Crear un equipo ficticio
        mock_team = Team.objects.create(name='Test Team', leader=self.user)
        mock_request = MagicMock(id= 1, spec=AdvanceLegalization)
        mock_request.status = "EN REVISIÓN"
        mock_request.__class__ = AdvanceLegalization
        mock_request.fullname = "ernesto"
        mock_request.cost_center = "010202"
        mock_request.bank = "Bancolombia"
        mock_request.account_type = "Ahorros" 
        mock_get_request_by_id.return_value = mock_request

        request = self.factory.get('/assign_request/1')
        request.user = self.user

        response = assign_request(request, mock_request.id)
        self.assertEqual(response.status_code, 200)  # Debería renderizar la página correctamente


    @patch('apps.internalRequests.views.get_request_by_id')
    def test_assign_request_get_bil(self, mock_get_request_by_id):
        # Crear una solicitud ficticia
        mock_request = BillingAccount.objects.create(member=self.user, request_date=timezone.now())

        # Crear un equipo ficticio
        mock_team = Team.objects.create(name='Test Team', leader=self.user)
        mock_request = MagicMock(id= 1, spec=BillingAccount)
        mock_request.status = "EN REVISIÓN"
        mock_request.__class__ = BillingAccount
        mock_request.fullname = "ernesto"
        mock_request.cost_center = "010202"
        mock_request.bank = "Bancolombia"
        mock_request.account_type = "Ahorros" 
        mock_get_request_by_id.return_value = mock_request

        request = self.factory.get('/assign_request/1')
        request.user = self.user

        response = assign_request(request, mock_request.id)
        self.assertEqual(response.status_code, 200)  # Debería renderizar la página correctamente
        
    @patch('apps.internalRequests.views.get_request_by_id')
    def test_assign_request_get_req(self, mock_get_request_by_id):
        # Crear una solicitud ficticia
        mock_request = Requisition.objects.create(member=self.user, request_date=timezone.now(), signature_status=True)

        # Crear un equipo ficticio
        mock_team = Team.objects.create(name='Test Team', leader=self.user)
        mock_request = MagicMock(id= 1, spec=Requisition)
        mock_request.status = "EN REVISIÓN"
        mock_request.__class__ = Requisition
        mock_request.fullname = "ernesto"
        mock_request.cost_center = "010202"
        mock_request.bank = "Bancolombia"
        mock_request.account_type = "Ahorros" 
        mock_get_request_by_id.return_value = mock_request

        request = self.factory.get('/assign_request/1')
        request.user = self.user

        response = assign_request(request, mock_request.id)
        self.assertEqual(response.status_code, 200)  # Debería renderizar la página correctamente

    @patch('apps.internalRequests.views.get_request_by_id')
    def test_assign_request_get_travex(self, mock_get_request_by_id):
        # Crear una solicitud ficticia
        mock_request = TravelExpenseLegalization.objects.create(
            member=self.user, 
            request_date=timezone.now(), 
            departure_date=timezone.now(), 
            return_date=timezone.now() + timedelta(days=7), 
            total1=1, total2=2, total3=2, 
            advance_total1=3,advance_total2=3,advance_total3=3,
            employee_balance1 = 2,
            employee_balance2 = 1,
            employee_balance3 = 4,
            icesi_balance1 = 3,
            icesi_balance2 = 2,
            icesi_balance3 = 1,
            signature_status = True,
            bank = "Bancolombial",
            account_type = "Corriente",
            account_number = "84658956541",

            )

        # Crear un equipo ficticio
        mock_team = Team.objects.create(name='Test Team', leader=self.user)
        mock_request = MagicMock(id= 1, spec=TravelExpenseLegalization)
        mock_request.status = "EN REVISIÓN"
        mock_request.__class__ = TravelExpenseLegalization
        mock_request.fullname = "ernesto"
        mock_request.cost_center = "010202"
        mock_request.bank = "Bancolombia"
        mock_request.account_type = "Ahorros" 
        mock_get_request_by_id.return_value = mock_request

        request = self.factory.get('/assign_request/1')
        request.user = self.user

        response = assign_request(request, mock_request.id)
        self.assertEqual(response.status_code, 200)  # Debería renderizar la página correctamente

        
    def test_travel_advance_request(self):
        # Crear una solicitud ficticia
        mock_request = TravelAdvanceRequest.objects.create(member=self.user, request_date=timezone.now(), departure_date=timezone.now(), return_date=timezone.now() + timedelta(days=7))

        request = self.factory.post('/travel_advance_request', {'id': mock_request.id, 'dateCheck': 'on'})
        request.user = self.user

        response = travel_advance_request(request)
        self.assertEqual(response.status_code, 302)  # Redirección después de la revisión

        # Verificar que la solicitud fue revisada
        mock_request.refresh_from_db()
        self.assertTrue(mock_request.is_reviewed)

        # Verificar que los datos de revisión son correctos
        review_data = mock_request.review_data
        self.assertEqual(len(review_data), 1022)  


    def test_travel_expense_legalization(self):
        # Crear una solicitud ficticia
        mock_request = TravelExpenseLegalization.objects.create(
            member=self.user, 
            request_date=timezone.now(), 
            departure_date=timezone.now(), 
            return_date=timezone.now() + timedelta(days=7), 
            total1=1, total2=2, total3=2, 
            advance_total1=3,advance_total2=3,advance_total3=3,
            employee_balance1 = 2,
            employee_balance2 = 1,
            employee_balance3 = 4,
            icesi_balance1 = 3,
            icesi_balance2 = 2,
            icesi_balance3 = 1,
            signature_status = True,
            bank = "Bancolombial",
            account_type = "Corriente",
            account_number = "84658956541",

            )

        request = self.factory.post('/travel_expense_legalization', {'id': mock_request.id, 'dateCheck': 'on'})
        request.user = self.user

        response = travel_expense_legalization(request)
        self.assertEqual(response.status_code, 302)  # Redirección después de la revisión

        # Verificar que la solicitud fue revisada
        mock_request.refresh_from_db()
        self.assertTrue(mock_request.is_reviewed)

        # Verificar que los datos de revisión son correctos
        review_data = mock_request.review_data
        self.assertEqual(len(review_data), 1019) 

    def test_advance_legalization(self):
        # Crear una solicitud ficticia
        mock_request = AdvanceLegalization.objects.create(
            member=self.user, request_date=timezone.now(),
              total=2, advance_total=2,  employee_balance_value= 
              2,icesi_balance_value=2, 
              signature_status=True,
                dependence = "8465",
                cost_center = "010202",
                purchase_reason = "lol",
                bank = "Bancolombia",
                account_type = "Ahorros",
                account_number = "5851645"
              )

        request = self.factory.post('/advance_legalization', {'id': mock_request.id, 'dateCheck': 'on'})
        request.user = self.user

        response = advance_legalization(request)
        self.assertEqual(response.status_code, 302)  # Redirección después de la revisión

        # Verificar que la solicitud fue revisada
        mock_request.refresh_from_db()
        self.assertTrue(mock_request.is_reviewed)

        # Verificar que los datos de revisión son correctos
        review_data = mock_request.review_data
        self.assertEqual(len(review_data), 813) 


    def test_billing_account(self):
        # Crear una solicitud ficticia
        mock_request = BillingAccount.objects.create(member=self.user, request_date=timezone.now())
        mock_request.user = self.user

        request = self.factory.post('/billing_account/', {'id': mock_request.id, 'dateCheck': 'on'})
        request.user = self.user

        response = billing_account(request)
        self.assertEqual(response.status_code, 302)  # Redirección después de la revisión

    def test_requisition(self):
        # Crear una solicitud ficticia
        mock_request = Requisition.objects.create(member=self.user, request_date=timezone.now(), signature_status=True)
        mock_request.user = self.user

        request = self.factory.post('/requisition/', {'id': '1', 'dateCheck': 'on'})
        request.user = self.user

        response = requisition(request)
        self.assertEqual(response.status_code, 302)  # Redirección después de la revisión

    @patch('apps.forms.models.Requisition.objects.get')
    def test_update_request_travel_advance_request(self, mock_get):
        # Crear una solicitud ficticia
        mock_request = TravelAdvanceRequest.objects.create(member=self.user, request_date=timezone.now(), departure_date=timezone.now(), return_date=timezone.now() + timedelta(days=7))
        mock_request.user = self.user

        mock_get.return_value = mock_request

        request = self.factory.post('/update_request/', {'id': mock_request.id, 'dateCheck': 'on'})
        request.user = self.user

        response = update_request(request, mock_request.id)
        self.assertEqual(response.status_code, 200)  # 200 status code means success

    @patch('apps.forms.models.Requisition.objects.get')
    def test_update_request_advance_legalization(self, mock_get):
        # Crear una solicitud ficticia
        mock_request = AdvanceLegalization.objects.create(
            member=self.user, request_date=timezone.now(),
              total=2, 
              advance_total=2,  
              employee_balance_value= 2,
              icesi_balance_value=2, 
              signature_status=True,
                dependence = "8465",
                cost_center = "010202",
                purchase_reason = "lol",
                bank = "Bancolombia",
                account_type = "Ahorros",
                account_number = "5851645"
              )
    
        mock_request.user = self.user

        mock_get.return_value = mock_request

        request = self.factory.post('/update_request/', {'id': mock_request.id, 'dateCheck': 'on','airportTransport': '100', 
            'localTransport': '200', 
            'food': '300', 
            'icesiBalanceValue': '400', 
            'employeeBalanceValue': '500', 
            'others': '600', 
            'total': '700',
            'advanceTotal': '700'})
        request.user = self.user

        response = update_request(request, mock_request.id)
        self.assertEqual(response.status_code, 200)  # 200 status code means success

    @patch('apps.forms.models.Requisition.objects.get')
    def test_update_request_travel_expense_legalization(self, mock_get):
        # Crear una solicitud ficticia
        mock_request = TravelExpenseLegalization.objects.create(
            member=self.user, 
            request_date=timezone.now(), 
            departure_date=timezone.now(), 
            return_date=timezone.now() + timedelta(days=7), 
            total1=1, total2=2, total3=2, 
            advance_total1=3,advance_total2=3,advance_total3=3,
            employee_balance1 = 2,
            employee_balance2 = 1,
            employee_balance3 = 4,
            icesi_balance1 = 3,
            icesi_balance2 = 2,
            icesi_balance3 = 1,
            signature_status = True,
            bank = "Bancolombial",
            account_type = "Corriente",
            account_number = "84658956541",
            )
        post_data = {
            'id': '1', 
            'total1': '100', 
            'total2': '200', 
            'total3': '300', 
            'advanceTotal1': '400', 
            'advanceTotal2': '500', 
            'advanceTotal3': '600', 
            'employeeBalance1': '700', 
            'employeeBalance2': '800', 
            'employeeBalance3': '900', 
            'icesiBalance1': '1000', 
            'icesiBalance2': '1100', 
            'icesiBalance3': '1200'
        }
        mock_request.total1=2
        mock_request.save()
        mock_request.user = self.user
        mock_get.return_value = mock_request

        request = self.factory.post(f'/update_request/{mock_request.id}', post_data)
        request.user = self.user

        response = update_request(request, mock_request.id)
        self.assertEqual(response.status_code, 200)  # 200 status code means success
