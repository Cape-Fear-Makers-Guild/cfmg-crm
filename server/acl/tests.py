import json

from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from members.models import Tag, User
from gandalf.decorators import HEADER
from .models import Machine, PermitType


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

    def call_acl_check_result(self, payload, expected_json):
        self.client.force_login(user=self.superuser)
        response = self.client.post(reverse("acl-v1-getok"), payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")

        json_content = json.loads(response.content)
        for key, value in expected_json.items():
            self.assertEqual(value, json_content[key])
        self.client.logout()

    def test_missing_form_denies_access(self):
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

        payload = {"tag": test_tag, "machine": test_machine}
        expected_json = {
            # Important bits
            "access": False,
            "requires_form": True,
            "missing_form": True,
            # Not really relevant for this test
            "requires_permit": False,
            "missing_permit": False,
            "out_of_order": False,
        }
        self.call_acl_check_result(payload, expected_json)

    def test_has_form_allows_access(self):
        test_tag = "1-2-4"
        Tag.objects.create(
            tag=test_tag,
            owner=self.user_form,
        )

        test_machine = "test-machine"
        mach = Machine.objects.create(
            name=test_machine.upper(),
            node_machine_name=test_machine,
            requires_form=True,
        )

        payload = {"tag": test_tag, "machine": test_machine}
        expected_json = {
            # Important bits
            "access": True,
            "requires_form": True,
            "missing_form": False,
            # Not really relevant for this test
            "requires_permit": False,
            "missing_permit": False,
            "out_of_order": False,
        }
        self.call_acl_check_result(payload, expected_json)

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

        # Test that setting the bearer token works without logging in
        header = {HEADER: settings.UT_BEARER_SECRET}
        response = self.client.post(
            reverse("acl-v1-getok"), payload, content_type="application/json", **header
        )
        self.assertEqual(response.status_code, 200)

        # Test that logging in as an admin works
        self.client.force_login(user=self.superuser)
        response = self.client.post(
            reverse("acl-v1-getok"), payload, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.client.logout()
