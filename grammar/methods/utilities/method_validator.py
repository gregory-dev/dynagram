
from .Errors import Errors

def method_validator(info=None, request=None):
  errors = Errors()

  def get_and_validate_argument(argument):
    if argument is None:
      return None

    from_request = request.GET.get(argument)

    if from_request is None:
      if errors is not None:
        errors.add('{} is missing.'.format(argument))

      return None

    if info is None or 'requirements' not in info:
      return from_request

    info_type = info.get('requirements').get(argument).get('type')

    if info_type is None:
      return from_request

    if info_type != type(from_request).__name__:
      errors.add('Argument {} with value <{}> is not of type <{}>.'.format(argument, from_request, info_type))

    return from_request

  return get_and_validate_argument, errors
