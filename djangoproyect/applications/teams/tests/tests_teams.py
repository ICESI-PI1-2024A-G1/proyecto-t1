import random
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.middleware.csrf import get_token
from applications.teams.models import Team
from faker import Faker
from django.contrib.auth import authenticate, login, logout

User = get_user_model()
fake = Faker()


class TeamTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.users = []
        self.teams = []

        self.user = User.objects.create_user(
            id="admin",
            username="admin",
            email="test@example.com",
            first_name="admin",
            password="password",
            is_staff=True,
        )

        for i in range(10):
            user = User.objects.create(
                id=f"0000{i}",
                username=f"0000{i}",
                password="123",
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )
            self.users.append(user)

        for i in range(5):
            leader = self.users[1]
            leader.is_leader = True
            leader.save()
            team = Team.objects.create(
                name=fake.company(), description=fake.text(), leader=leader
            )
            team_members = random.sample(
                [user for user in self.users if user != leader], random.randint(3, 5)
            )
            team.members.add(*team_members)
            self.teams.append(team)
        self.client.login(id="admin", password="password")

    def test_show_teams_many(self):
        response = self.client.get(reverse("teams:show_teams"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["teams"]), len(Team.objects.all()))

    def test_show_teams_empty(self):
        Team.objects.all().delete()
        response = self.client.get(reverse("teams:show_teams"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["teams"]), len(Team.objects.all()))

    def test_show_teams_unauthorized(self):
        self.client.logout()
        response = self.client.get(reverse("teams:show_teams"))
        self.assertRedirects(response, "/logout/?next=/teams/", 302)

    def test_show_teams_leader(self):
        self.user.is_staff = False
        self.user.save()
        teams = Team.objects.all()
        for i in range(3):
            self.teams[i].leader = self.user
            self.teams[i].save()
        response = self.client.get(reverse("teams:show_teams"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["teams"]), 3)
