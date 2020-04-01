
from django.http import HttpResponse
from django.test import TestCase

from ..decoy import decoy

class DecoyTestCase(TestCase):
  def test_render(self):
    class mock_request:
      GET = {
        'required_type': 'word',
        'truth': 'truth',
        'decoy': 'decoy',
        'slot_value': 'slot_value',
      }

    result = decoy(mock_request)

    self.assertIsInstance(result, HttpResponse)
