import unittest
from urllib.request import Request
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.test.client import RequestFactory
from django.urls import reverse
from apps.login.backends import IDBackend
from apps.teams.models import Team
from utils.models import CustomUser
from ..views import show_teams, add_team, edit_team, delete_team, show_members
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.auth.models import User


class IDBackendTest(unittest.TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.backend = IDBackend()
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )

    def test_authenticate_with_valid_credentials(self):
        request = self.factory.post("/")
        user = self.backend.authenticate(
            request, id=self.user.id, password="testpassword"
        )
        self.assertEqual(user, self.user)

    def test_authenticate_with_invalid_credentials(self):
        request = self.factory.post("/")
        user = self.backend.authenticate(
            request, id=self.user.id, password="wrongpassword"
        )
        self.assertIsNone(user)

    def test_get_user_with_valid_id(self):
        user = self.backend.get_user(self.user.id)
        self.assertEqual(user, self.user)

    def test_get_user_with_invalid_id(self):
        user = self.backend.get_user(9999)
        self.assertIsNone(user)


class TeamViewsTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            id="12345", password="12345", email="testuser@example.com", is_leader=True
        )

    def test_show_teams_superuser(self):
        request = self.factory.get("/")
        request.user = self.user
        request.user.is_superuser = True
        response = show_teams(request)
        self.assertEqual(response.status_code, 200)

    def test_show_teams_non_superuser(self):
        request = self.factory.get("/")
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.user
        request.user.is_superuser = False

        # Crear un equipo liderado por el usuario
        team = Team.objects.create(name="Test Team", leader=self.user)

        response = show_teams(request)
        self.assertEqual(response.status_code, 200)

        # Verificar que el equipo correcto se está mostrando
        self.assertContains(response, "Test Team")

    def test_add_team_get(self):
        request = self.factory.get("/")
        request.user = self.user
        response = add_team(request)
        self.assertEqual(response.status_code, 200)

    def test_add_team_post(self):
        self.factory = RequestFactory()
        request = self.factory.post(
            "/",
            {
                "name": "Test Team",
                "leader": self.user.id,
                "description": "Test description",
                "form_type": "Test Form Type",
                "member-1": "on",
                "member-2": "on",
            },
        )
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.user
        response = add_team(request)
        self.assertEqual(response.status_code, 302)

    def test_edit_team_get(self):
        # Create a team
        team = Team.objects.create(name="Test Team", leader=self.user)

        request = self.factory.get("/")
        request.user = self.user

        # Edit the team
        response = edit_team(request, team.id)
        self.assertEqual(response.status_code, 200)

    def test_edit_team_post(self):
        # Create a team
        team = Team.objects.create(name="Test Team", leader=self.user)

        request = self.factory.post(
            "/",
            {
                "name": "Updated Team Name",
                "leader": self.user.id,
                "description": "Updated description",
                "form_type": "Updated Form Type",
                "member-1": "on",
                "member-2": "on",
            },
        )
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.user

        # Edit the team
        response = edit_team(request, team.id)
        self.assertEqual(response.status_code, 302)

    def test_edit_team_post_with_assigned_members(self):
        # Create a team
        team = Team.objects.create(name="Test Team", leader=self.user)

        # Create another user to be a member
        member_user = CustomUser.objects.create_user(
            id="test_member",
            username="member",
            password="password",
            email="test@example.com",
        )

        # Add the member to the team
        team.members.add(member_user)

        temp_member_id = f"member-{str(member_user.id)}"

        request = self.factory.post(
            reverse("teams:edit_team", args=[team.id]),
            {
                "name": "Updated Team Name",
                "leader": self.user.id,
                "description": "Updated description",
                "form_type": "Updated Form Type",
                "member_id": [temp_member_id],
            },
        )
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.user
        print(request)
        print(request.POST)

        # Edit the team
        response = edit_team(request, team.id)

        # Check that the team's fields were updated
        self.assertEqual(team.leader, self.user)
        self.assertEqual(team.name, "Test Team")
        self.assertEqual(team.description, "")
        self.assertEqual(team.typeForm, "")

    def test_delete_team(self):
        # Create a team
        team = Team.objects.create(name="Test Team", leader=self.user)

        request = self.factory.delete("/")
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.user

        # Delete the team
        response = delete_team(request, team.id)
        self.assertEqual(response.status_code, 200)

        # Verify the team was deleted
        with self.assertRaises(Team.DoesNotExist):
            Team.objects.get(id=team.id)

    def test_show_members(self):
        # Create a team
        team = Team.objects.create(name="Test Team", leader=self.user)

        request = self.factory.get("/")
        request.user = self.user

        # Show the team members
        response = show_members(request, team.id)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
