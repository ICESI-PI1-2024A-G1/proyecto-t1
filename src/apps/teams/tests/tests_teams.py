"""
Request Test

This module contains test cases for the views related to teams in the application.
"""

import random
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.middleware.csrf import get_token
from apps.teams.models import Team
from faker import Faker
from django.contrib.auth import authenticate, login, logout

from apps.teams.forms import TeamForm

User = get_user_model()
fake = Faker()


class TeamTestCase(TestCase):
    """
    TestCase class for testing the Teams app.

    Attributes:
        client (Client): Django test client for making requests.
        users (list): List of User instances created for testing.
        teams (list): List of Team instances created for testing.
        user (User): User instance representing the admin user for testing.
        leaders (list): List of User instances representing team leaders.
        form_data (dict): Dictionary representing form data for testing.
    """

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

        for i in range(30):
            user = User.objects.create(
                id=f"0000{i}",
                username=f"0000{i}",
                password="123",
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )
            self.users.append(user)

        self.leaders = [self.user]
        for i in range(5):
            leader = random.choice(
                User.objects.exclude(id__in=[leader.id for leader in self.leaders])
            )
            leader.is_leader = True
            leader.save()
            self.leaders.append(leader)
            team = Team.objects.create(
                name=fake.company(),
                description=fake.text(max_nb_chars=100),
                leader=leader,
            )
            team_members = random.sample(
                [user for user in self.users if user != leader], random.randint(3, 5)
            )
            team.members.add(*team_members)
            self.teams.append(team)

        leader = random.choice(
            User.objects.exclude(id__in=[leader.id for leader in self.leaders])
        )
        leader.is_leader = True
        leader.save()
        self.leaders.append(leader)
        team_members = random.sample(
            [user for user in self.users if user != leader], random.randint(3, 5)
        )

        self.form_data = {
            "name": fake.company(),
            "description": fake.text(max_nb_chars=100),
            "leader": leader.id,
            "members": [u.id for u in team_members],
        }

        self.client.login(id="admin", password="password")

    ### SHOW TEAMS TESTS

    def test_show_teams_many(self):
        """
        Tests displaying all teams when many teams exist.
        """
        response = self.client.get(reverse("teams:show_teams"))
        self.assertEqual(response.status_code, 200)
        displayed_teams = [member.id for member in response.context["teams"]]
        all_teams = [member.id for member in Team.objects.all()]
        self.assertEqual(displayed_teams, all_teams)
        self.assertTemplateUsed("teams:show-teams.html")

    def test_show_teams_empty(self):
        """
        Tests displaying teams when no teams exist.
        """
        Team.objects.all().delete()
        response = self.client.get(reverse("teams:show_teams"))
        self.assertEqual(response.status_code, 200)
        displayed_teams = [member.id for member in response.context["teams"]]
        all_teams = [member.id for member in Team.objects.all()]
        self.assertEqual(displayed_teams, all_teams)
        self.assertTemplateUsed("teams:show-teams.html")

    def test_show_teams_unauthorized(self):
        """
        Test displaying teams when the user is not authorized.
        """
        self.client.logout()
        response = self.client.get(reverse("teams:show_teams"))
        self.assertRedirects(response, "/logout/?next=/teams/", 302)
        self.assertTemplateUsed("login:login.html")

    def test_show_teams_leader(self):
        """
        Test displaying teams for a user who is a leader.
        """
        self.user.is_staff = False
        self.user.save()
        teams = [team.id for team in Team.objects.filter(leader=self.user)]
        response = self.client.get(reverse("teams:show_teams"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("teams:show-teams.html")
        displayed_teams = [team.id for team in response.context["teams"]]
        self.assertEqual(displayed_teams, teams)

    ### ADD TEAM TESTS

    def test_add_team_form_authenticated(self):
        """
        Test displaying the add team form when the user is authenticated.
        """
        response = self.client.get(reverse("teams:add_team"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("teams:add-team.html")
        self.assertIsNotNone(response.context["form"])

    def test_add_team_form_unauthorized(self):
        """
        Test accessing the add team form when the user is not authorized.
        """
        self.client.logout()
        response = self.client.get(reverse("teams:add_team"))
        self.assertRedirects(response, "/logout/?next=/teams/add-team-form/", 302)
        self.assertTemplateUsed("login:login.html")

    def test_add_team_form_unauthorized(self):
        """
        Test posting data to the add team form when the user is not authorized.
        """
        self.client.logout()
        response = self.client.post(reverse("teams:add_team"))
        self.assertRedirects(response, "/logout/?next=/teams/add-team-form/", 302)
        self.assertTemplateUsed("login:login.html")

    def test_add_team_all_valid_fields(self):
        """
        Test adding a team with all valid fields.
        """
        prev_teams_number = Team.objects.count()
        form = TeamForm(self.form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse("teams:add_team"), self.form_data)
        self.assertRedirects(response, "/teams/", 302)
        self.assertEqual(Team.objects.count(), prev_teams_number + 1)

    def test_add_team_no_leader(self):
        """
        Test adding a team without a leader.
        """
        self.form_data.pop("leader")
        prev_teams_number = Team.objects.count()
        form = TeamForm(self.form_data)
        self.assertFalse(form.is_valid())
        response = self.client.post(reverse("teams:add_team"), self.form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("teams:add-team.html")
        self.assertEqual(Team.objects.count(), prev_teams_number)

    def test_add_team_no_members(self):
        """
        Test adding a team without any members.
        """
        self.form_data["members"] = []
        prev_teams_number = Team.objects.count()
        form = TeamForm(self.form_data)
        self.assertFalse(form.is_valid())
        response = self.client.post(reverse("teams:add_team"), self.form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("teams:add-team.html")
        self.assertEqual(Team.objects.count(), prev_teams_number)

    ### EDIT TEAM TESTS

    def test_edit_team_form_authenticated(self):
        """
        Test displaying the edit team form when the user is authenticated.
        """
        response = self.client.get(reverse("teams:edit_team", args=[self.teams[0].id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("teams:edit-team.html")
        self.assertIsNotNone(response.context["form"])

    def test_edit_team_form_unauthorized(self):
        """
        Test accessing the edit team form when the user is not authorized.
        """
        self.client.logout()
        response = self.client.get(reverse("teams:edit_team", args=[self.teams[0].id]))
        self.assertRedirects(
            response, f"/logout/?next=/teams/edit-team/{self.teams[0].id}/", 302
        )
        self.assertTemplateUsed("login:login.html")

    def test_edit_team_not_found(self):
        """
        Test accessing the edit team form for a non-existent team.
        """
        response = self.client.get(reverse("teams:edit_team", args=[300]))
        self.assertTemplateUsed("errorHandler:error_404_view.html")

    def test_edit_team_all_valid_fields(self):
        """
        Test editing a team with all valid fields.
        """
        form = TeamForm(self.form_data, instance=self.teams[0])
        self.assertTrue(form.is_valid())
        response = self.client.post(
            reverse("teams:edit_team", args=[self.teams[0].id]), self.form_data
        )
        self.assertRedirects(response, "/teams/", 302)
        self.assertEqual(self.teams[0].name, self.form_data["name"])

    def test_edit_team_no_leader(self):
        """
        Test editing a team without a leader.
        """
        form_data = {
            "name": "Updated Team Name",
            "description": "Updated Team Description",
            "members": [self.user.id],
        }
        form = TeamForm(form_data, instance=self.teams[0])
        self.assertFalse(form.is_valid())
        response = self.client.post(
            reverse("teams:edit_team", args=[self.teams[0].id]), form_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("teams:edit-team.html")
        self.teams[0].refresh_from_db()
        self.assertNotEqual(self.teams[0].name, "New name")

    def test_edit_team_no_members(self):
        """
        Test editing a team without any members.
        """
        form_data = {
            "name": "Updated Team Name",
            "description": "Updated Team Description",
            "leader": self.user.id,
            "members": [],
        }
        form = TeamForm(form_data, instance=self.teams[0])
        self.assertFalse(form.is_valid())
        response = self.client.post(
            reverse("teams:edit_team", args=[self.teams[0].id]), form_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("teams:edit-team.html")
        self.teams[0].refresh_from_db()
        self.assertNotEqual(self.teams[0].name, "New Name")

    ### DELETE TEAM TESTS

    def test_delete_team_not_found(self):
        """
        Test deleting a non-existent team.
        """
        response = self.client.delete(reverse("teams:edit_team", args=[300]))
        self.assertTemplateUsed("errorHandler:error_404_view.html")

    def test_delete_team_valid(self):
        """
        Test deleting an existing team.
        """
        prev_teams_count = Team.objects.count()
        response = self.client.delete(
            reverse("teams:delete_team", args=[self.teams[0].id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Team.objects.count(), prev_teams_count - 1)
        self.assertFalse(Team.objects.filter(id=self.teams[0].id).exists())

    ### SHOW MEMBERS TESTS

    def test_show_members_authenticated(self):
        """
        Test displaying members of a team when the user is authenticated.
        """
        members = [member.id for member in self.teams[0].members.all()]
        response = self.client.get(
            reverse("teams:show_members", args=[self.teams[0].id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("teams:show-members.html")
        displayed_members = response.context["members"]
        displayed_members = [member.id for member in displayed_members]
        self.assertEqual(members, displayed_members)

    def test_show_members_not_found(self):
        """
        Test accessing members of a non-existent team.
        """
        response = self.client.get(reverse("teams:show_members", args=[300]))
        self.assertTemplateUsed("errorHandler:error_404_view.html")

    def test_show_members_unauthorized(self):
        """
        Test accessing members of a team when the user is not authorized.
        """
        self.client.logout()
        response = self.client.get(
            reverse("teams:show_members", args=[self.teams[0].id])
        )
        self.assertRedirects(
            response, f"/logout/?next=/teams/show-members/{self.teams[0].id}", 302
        )
        self.assertTemplateUsed("login:login.html")
