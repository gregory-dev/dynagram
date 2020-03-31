
from django.http import HttpResponse

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

def decoy(request):
  required_type = request.GET.get('required_type')
  truth = request.GET.get('truth')
  decoy = request.GET.get('decoy')
  slot_value = request.GET.get('slot_value')
  rendered_grammar = grammar.format(
    required_type=required_type,
    truth=truth,
    decoy=decoy,
    slot_value=slot_value,
  )

  return HttpResponse(rendered_grammar)

decoy.requirements = {
  'required_type': {
    'type': 'string',
    'options': {
      'word': 'A single word',
    },
  },
  'truth': 'A string representing the truth value',
  'decoy': 'A string representing the decoy value',
  'slot_value': 'A string',
}
