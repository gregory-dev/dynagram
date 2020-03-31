
from django.http import HttpResponse

def test_method(request):
  print(request)

  return HttpResponse('test_method')

test_method.requirements = {
  'args': 'An array of arguments',
}
