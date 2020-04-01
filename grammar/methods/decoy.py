
from django.http import HttpResponse, JsonResponse

grammar = '''
<?xml version="1.0" encoding="ISO-8859-1" ?>
<grammar
  version="1.0"
  xmlns="http://www.w3.org/2001/06/grammar"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.w3.org/2001/06/grammar http://www.w3.org/TR/speech-grammar/grammar.xsd"
  xml:lang="en-US" mode="voice" root="root"
>
  <!-- ############################################## -->
  <meta name="Parameters" content="" />
  <meta name="ASR_Engine" content="Nuance" />
  <meta name="Language" content="en-US" />
  <meta name="Description" content="This grammar handles a caller's word input." />
  <meta name="ASR_Version" content="9.x" />
  <!-- ############################################## -->
  <rule id="root" scope="public">
    <!-- <item repeat="0-1"><ruleref uri="#umUh"/></item> -->
    <one-of>
      <item weight="0.99">
        <item>
          <ruleref uri="#realITEMS"/>
          <tag>CHOICE=realITEMS.RETVAL</tag>
        </item>
      </item>
      <item weight="0.01">
        <item>
          <ruleref uri="#decoyITEMS"/>
          <tag>CHOICE=decoyITEMS.RETVAL</tag>
        </item>
      </item>
    </one-of>
  </rule>
  <rule id="realITEMS">
    <one-of>
      <item>{truth}<tag>RETVAL=&apos;{slot_value}&apos;</tag></item>
    </one-of>
  </rule>
  <!-- ### Decoy Grammar ### -->
  <rule id="decoyITEMS">
    <one-of>
      <item>{decoy}<tag>RETVAL=&apos;Dummy&apos;</tag></item>
    </one-of>
  </rule>
  <rule id="digit_zero">
    <one-of>
      <item>zero</item>
      <item>oh</item>
      <!--<item>nil</item>
      <item>naught</item>
      <item>null</item> -->
    </one-of>
  </rule>
</grammar>
'''

decoy_info = {
  'description': 'The decoy method',
  'requirements': {
    'required_type': {
      'type': 'str',
      'options': {
        'word': 'A single word',
      },
    },
    'truth': {
      'type': 'str',
      'description': 'A string representing the truth value',
    },
    'decoy': {
      'type': 'str',
      'description': 'A string representing the decoy value',
    },
    'slot_value': {
      'type': 'str',
      'description': 'A string',
    }
  }
}

class Errors:
  def __init__(self):
    self.messages = []

  def add(self, message):
    self.messages.append(message)

  def render(self):
    return JsonResponse({
      'errors': self.messages,
    })

def get_and_validate_argument(info=None, errors=None, request=None, argument=None):
  if argument is None or request is None:
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

def decoy(request):
  errors = Errors()
  kwargs = {
    'info': decoy_info,
    'errors': errors,
    'request': request,
  }

  required_type = get_and_validate_argument(**kwargs, argument='required_type')
  truth = get_and_validate_argument(**kwargs, argument='truth')
  decoy = get_and_validate_argument(**kwargs, argument='decoy')
  slot_value = get_and_validate_argument(**kwargs, argument='slot_value')
  rendered_grammar = grammar.format(
    required_type=required_type,
    truth=truth,
    decoy=decoy,
    slot_value=slot_value,
  )

  if errors.messages:
    return errors.render()

  return HttpResponse(rendered_grammar)

decoy.info = decoy_info
