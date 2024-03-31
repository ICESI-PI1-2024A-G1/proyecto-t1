from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from applications.teams.models import Team


class TeamTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            first_name="belso",
            last_name="muchacho",
            password="testpassword",
        )
        self.user2 = User.objects.create_user(
            username="user2",
            first_name="yuluka",
            last_name="gigante",
            password="testpassword",
        )
        self.team = Team.objects.create(
            name="Test Team",
            description="Test description",
            leader=self.user1,
        )
        self.team.members.add(self.user2)
        self.client.login(username="user1", password="testpassword")

    def test_add_member_view(self):
        print(self.team)
        response = self.client.get(reverse("add_member", args=[self.team.id]))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("add_member", args=[self.team.id]),
            {"users[]": [self.user1.id]},
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "message": "Miembros añadidos con éxito al equipo.",
                "users": [
                    {
                        "first_name": self.user1.first_name,
                        "last_name": self.user1.last_name,
                        "id": self.user1.id,
                        "username": self.user1.username,
                    }
                ],
            },
        )

    def test_delete_member_view(self):
        response = self.client.delete(
            reverse("delete_member", args=[self.team.id, self.user2.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"message": "El miembro 2 ha sido eliminado correctamente"},
        )

    def test_add_team_view(self):
        response = self.client.get(reverse("add_team"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add-team.html")

        csrf_token = response.cookies["csrftoken"].value

        response = self.client.post(
            reverse("add_team"),
            {
                "name": "New Test Team",
                "description": "New test description",
                "leader": self.user2.id,
                "members": [],
                "csrfmiddlewaretoken": csrf_token,
            },
        )

    def test_delete_team_view(self):
        response = self.client.delete(reverse("delete_team", args=[self.team.id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"message": f"El equipo {self.team.id} ha sido eliminado correctamente"},
        )
