from django.test import TestCase
from .models import clean_tag_string


class HelperTests(TestCase):
    def test_clean_tag_string(self):
        for tag in ["1-2-3", "d1-16-1f-19", "D1-16-1F-19"]:
            clean_tag = clean_tag_string(tag)
            self.assertEqual(clean_tag, tag)
        for dirty_tag in ["!1-2-3", "1-2", "1_2_3"]:
            clean_tag = clean_tag_string(dirty_tag)
            self.assertIsNone(clean_tag, None)
