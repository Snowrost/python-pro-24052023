import json

from django.test import TestCase
from django.urls import reverse


class IndexTestCase(TestCase):

    def test_index(self):
        # given
        url = reverse("index")

        # when
        response = self.client.get(url)

        # then
        self.assertJSONEqual(response.content, {"message": "hello"})

