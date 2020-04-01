
from django.http import JsonResponse

class Errors:
  def __init__(self):
    self.messages = []

  def add(self, message):
    self.messages.append(message)

  def render(self):
    return JsonResponse({
      'errors': self.messages,
    })
