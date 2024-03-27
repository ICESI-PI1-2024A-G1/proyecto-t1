from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from applications.requests.models import Requests
from datetime import date, timedelta


class RequestViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()

        # Create an admin user
        self.admin = self.user_model.objects.create_user(
            id='12345678',
            username='12345678',
            email='email1',
            password='testpassword',
            is_staff=True,
        )

        # Create a leader user
        self.leader = self.user_model.objects.create_user(
            id='123456789',
            username='12345678',
            email='email2',
            password='testpassword',
            is_leader=True,
        )

        # Create some requests
        self.requests = [
            Requests.objects.create(
                document='document{}'.format(i),
                applicant='applicant{}'.format(i),
                manager='manager{}'.format(i),
                description='description{}'.format(i),
                title='title{}'.format(i),
                initial_date=date.today(),
                final_date=date.today() + timedelta(days=1),
                past_days=0,
                status='status{}'.format(i),
                type='type{}'.format(i),
            )
            for i in range(5)
]

        # Assign the requests to the leader
        for request in self.requests:
            request.assigned_users.set([self.leader])


    def test_admin_sees_all_requests(self):
        self.client.login(id='12345678', password='testpassword')

        response = self.client.get('/requests/')

        # Ensure the admin sees all requests
        self.assertEqual(len(self.requests), len(response.context['requests']))


    def test_leader_sees_only_assigned_requests(self):
        self.client.login(id='123456789', password='testpassword')

        response = self.client.get('/requests/')

        # Get the number of requests assigned to the leader
        num_assigned_requests = self.leader.requests.count()

        # Ensure the number of requests in the response is equal to the number of requests assigned to the leader
        self.assertEqual(len(response.context['requests']), num_assigned_requests)