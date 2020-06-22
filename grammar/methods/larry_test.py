
from django.http import HttpResponse

from .utilities import method_validator

grammar = '{required_type}'

larry_test_info = {
  'description': 'The test method',
  'requirements': {
    'required_type': {
      'type': 'str',
      'options': {
        'word': 'A single word',
      },
    },
  }
}

def larry_test(request):
  validator, errors = method_validator(info=larry_test_info, request=request)

  required_type = validator('required_type')

  rendered_grammar = grammar.format(
    required_type=required_type,
  )

  if errors.messages:
    return errors.render()

  return HttpResponse(rendered_grammar)

larry_test.info = larry_test_info