import json

from django.test import TestCase
from django.urls import reverse

from members.models import Tag, User
from .models import Machine


class APIGetOkTests(TestCase):
    def setUp(self):
        self.user_noform = User.objects.create_user(
            email="noform@example.com", first_name="no", last_name="form"
        )
        self.user_form = User.objects.create_user(
            email="hasform@example.com",
            first_name="has",
            last_name="form",
            form_on_file=True,
        )
        self.superuser = User.objects.create_superuser(
            email="superuser@example.com",
            first_name="super",
            last_name="user",
            password="foo",
        )

    def test_missing_form_prevents_access(self):
        # TODO: also test with the bearer token
        self.client.force_login(user=self.superuser)

        # TODO: test also with user_form
        test_tag = "1-2-3"
        Tag.objects.create(
            tag=test_tag,
            owner=self.user_noform,
        )

        test_machine = "test-machine"
        mach = Machine.objects.create(
            name=test_machine.upper(),
            node_machine_name=test_machine,
            requires_form=True,
        )

        payload = {
            "tag": test_tag,
            "machine": test_machine,
        }

        response = self.client.post(reverse("acl-v1-getok"), payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")

        json_content = json.loads(response.content)
        self.assertFalse(json_content["access"])
        self.assertTrue(json_content["requires_form"])
        self.assertFalse(json_content["requires_permit"])
        self.assertTrue(json_content["missing_form"])
        self.assertFalse(json_content["missing_permit"])
        self.assertFalse(json_content["out_of_order"])
        self.client.logout()

    def test_auth_access_getok(self):
        # test that normal users cannot query the access API, only super users or bearer token
        payload = {
            "tag": "test-tag",
            "machine": "test-machine",
        }
        response = self.client.post(
            reverse("acl-v1-getok"), payload, content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)

        self.client.force_login(user=self.user_form)
        response = self.client.post(
            reverse("acl-v1-getok"), payload, content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)
        self.client.logout()
