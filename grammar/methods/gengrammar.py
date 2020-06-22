from django.http import HttpResponse
import re

from .utilities import method_validator

grammar = '''
<?xml version="1.0" encoding="ISO-8859-1" ?>
<grammar
  version="1.0"
  xmlns="http://www.w3.org/2001/06/grammar"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.w3.org/2001/06/grammar http://www.w3.org/TR/speech-grammar/grammar.xsd"
  xml:lang="{language}" mode="{mode}" root="root"
/>
  <!-- ############################################## -->
  <meta name="Parameters" content="" />
  <meta name="ASR_Engine" content="Nuance" />
  <meta name="Language" content="{language}" />
  <meta name="Description" content="This grammar handles a caller's {required_type} input." />
  <meta name="ASR_Version" content="9.x" />
  <!-- ############################################## -->
  <rule id="root" scope="public">
    <!-- <item repeat="0-1"><ruleref uri="#umUh"/></item> -->
    <one-of>
      <item weight="{weight}">
        <item>
          <ruleref uri="#realITEMS"/>
          <tag>{slot_name}=realITEMS.RETVAL</tag>
        </item>
      </item>

{decoyTopRule}

    </one-of>
  </rule>
  <rule id="realITEMS">
    <one-of>
        {truth}
    </one-of>
  </rule>
  
{decoy}

{addUpperGrammarList}

{addMiddleGrammarList}

{addLowerGrammarList}

</grammar>
'''


#<rule id="digit_zero">
#    <one-of>
#      <item>zero</item>
#      <item>oh</item>
#      <!--<item>nil</item>
#      <item>naught</item>
#      <item>null</item> -->
#    </one-of>
#  </rule>



def method_extractor(info=None, request=None):

  def get_argument(argument):
    if argument is None:
      return None

    from_request = request.GET.get(argument)

    if from_request is None:
      return None

    if info is None or 'requirements' not in info:
      return from_request

    info_type = info.get('optional').get(argument).get('type')

    if info_type is None:
      return from_request

    return from_request

  return get_argument

gengrammar_info = {
  'description': 'The decoy method',
  'requirementsmore ': {
    'required_type': {
      'type': 'str',
      'options': {
        'word': 'A single word',
      },
    },
    'truth': {
      'type': 'str',
      'description': 'A string representing the truth value',
    }
  }
}

optional_gengrammar_info = {
  'description': 'The decoy method',
  'optional': {
    'dweight': {
      'type': 'str',
      'description': 'A floating point number',
    },
    'slot_name': {
      'type': 'str',
      'description': 'A string',
    },
    'dtmf': {
      'type': 'str',
      'description': 'T of F: DTMF mode',
    },
    'dtmf_retvals': {
      'type': 'str',
      'description': 'T of F: DTMF mode',
    },
    'weight': {
      'type': 'str',
      'description': 'A floating point number',
    },
    'language': {
      'type': 'str',
      'description': 'Language',
    },
    'decoy': {
      'type': 'str',
      'description': 'A string representing the decoy value',
    }
  }
}

def buildRegularMultiLevel(strNumber, numLength, xCounter, hundredsSequenceDict, tripleOnesDict, generalOnesDict, generalTensDict, generalTeensDict, triplesLimitDict, startLimit, triplesNameDict, triplesNamePluralDict, actualTriplesLevel, prevTriplesLevel, prevlocstringNumber, greaterTensConnector, tensOnesConnector, language, allowAlternate, prevActive, thousandsSequenceDict):
  locstringNumber = prevlocstringNumber

  if 'es-' in language and allowAlternate == 1:

#Ones
    xCounter, locstringNumber = buildRegularOnesAlternate(strNumber, numLength, xCounter, tripleOnesDict, generalOnesDict, generalTensDict, generalTeensDict, startLimit, triplesNameDict, triplesNamePluralDict, actualTriplesLevel, locstringNumber, language, thousandsSequenceDict)

#Tens
    xCounter, locstringNumber = buildRegularTensAlternate(strNumber, numLength, xCounter, tripleOnesDict, generalOnesDict, generalTensDict, generalTeensDict, startLimit+1, triplesNameDict, triplesNamePluralDict,actualTriplesLevel, locstringNumber, tensOnesConnector, language, thousandsSequenceDict)

#Hundreds
    xCounter, locstringNumber, triplesLevel = buildRegularTriples(strNumber, numLength, xCounter, hundredsSequenceDict, tripleOnesDict, generalOnesDict, generalTensDict, generalTeensDict, triplesLimitDict, triplesNameDict, triplesNamePluralDict, prevTriplesLevel,locstringNumber, greaterTensConnector, tensOnesConnector, language)

  elif 'en-' in language or allowAlternate == 0:

#Ones
    xCounter, locstringNumber = buildRegularOnes(strNumber, numLength, xCounter, tripleOnesDict, generalOnesDict, generalTensDict, generalTeensDict, startLimit, triplesNameDict, triplesNamePluralDict, actualTriplesLevel, locstringNumber, language)

#Tens
    xCounter, locstringNumber = buildRegularTens(strNumber, numLength, xCounter, tripleOnesDict, generalOnesDict, generalTensDict, generalTeensDict, startLimit+1, triplesNameDict, triplesNamePluralDict,actualTriplesLevel, locstringNumber, tensOnesConnector, language)

#Hundreds
    xCounter, locstringNumber, triplesLevel = buildRegularTriples(strNumber, numLength, xCounter, hundredsSequenceDict, tripleOnesDict, generalOnesDict, generalTensDict, generalTeensDict, triplesLimitDict, triplesNameDict, triplesNamePluralDict, prevTriplesLevel,locstringNumber, greaterTensConnector, tensOnesConnector, language)

    if prevlocstringNumber != locstringNumber:
      prevActive = 1
    else:
      prevActive = 0

  return xCounter, locstringNumber, triplesLevel, prevActive


def buildRegularOnesAlternate(strNumber, numLength, xCounter, tripleOnesDict, generalOnesDict, generalTensDict, generalTeensDict, onesLimit, triplesNameDict, triplesNamePluralDict, prevTriplesLevel, prevlocstringNumber, language, thousandsSequenceDict):
  onesPart = ''
  locstringNumber = prevlocstringNumber
  if numLength == onesLimit:
    xCounter = xCounter - 1
    if strNumber[xCounter] == '1':
      onesPart = ' <item repeat="0-1"> ' + tripleOnesDict[strNumber[xCounter]] + ' </item> ' + ' ' + thousandsSequenceDict['1']
    else:
      onesPart = tripleOnesDict[strNumber[xCounter]] + ' ' + thousandsSequenceDict['1']
    locstringNumber = onesPart + locstringNumber

  return xCounter, locstringNumber


def buildRegularTensAlternate(strNumber, numLength, xCounter, tripleOnesDict, generalOnesDict, generalTensDict, generalTeensDict, tensLimit, triplesNameDict, triplesNamePluralDict, prevTriplesLevel, prevlocstringNumber, tensOnesConnector, language, thousandsSequenceDict):
  tensPart = ''
  locstringNumber = prevlocstringNumber
  if numLength == tensLimit:
    xCounter = xCounter - 2

    if strNumber[xCounter] != '0' and strNumber[xCounter+1] != '0':
      if strNumber[xCounter] == '1':
        tensPart = generalTeensDict[strNumber[xCounter+1]] + ' ' + thousandsSequenceDict['1']
      else:
        if tensOnesConnector != '':
          tensPart = generalTensDict[strNumber[xCounter]] + ' <item repeat="0-1">' + tensOnesConnector + '</item> ' + generalOnesDict[strNumber[xCounter+1]] + ' ' + thousandsSequenceDict['1']
        else:
          tensPart = generalTensDict[strNumber[xCounter]] + ' ' + generalOnesDict[strNumber[xCounter+1]] + ' ' + thousandsSequenceDict['1']
    else:
      tensPart = generalTensDict[strNumber[xCounter]] + ' ' + thousandsSequenceDict['1']

    locstringNumber = tensPart + prevlocstringNumber

  return xCounter, locstringNumber

def buildRegularOnes(strNumber, numLength, xCounter, tripleOnesDict, generalOnesDict, generalTensDict, generalTeensDict, onesLimit, triplesNameDict, triplesNamePluralDict, prevTriplesLevel, prevlocstringNumber, language):
  onesPart = ''
  locstringNumber = prevlocstringNumber
  if numLength == onesLimit:
    xCounter = xCounter - 1
    if strNumber[xCounter] == '1':
      onesPart = tripleOnesDict[strNumber[xCounter]] + ' ' + triplesNameDict[prevTriplesLevel] + ' '
    else:
      onesPart = tripleOnesDict[strNumber[xCounter]] + ' ' + triplesNamePluralDict[prevTriplesLevel] + ' '
    locstringNumber = onesPart + locstringNumber

  return xCounter, locstringNumber


def buildRegularTens(strNumber, numLength, xCounter, tripleOnesDict, generalOnesDict, generalTensDict, generalTeensDict, tensLimit, triplesNameDict, triplesNamePluralDict, prevTriplesLevel, prevlocstringNumber, tensOnesConnector, language):
  tensPart = ''
  locstringNumber = prevlocstringNumber
  if numLength == tensLimit:
    xCounter = xCounter - 2

    if strNumber[xCounter] != '0' and strNumber[xCounter+1] != '0':
      if strNumber[xCounter] == '1':
        tensPart = generalTeensDict[strNumber[xCounter+1]] + ' ' + triplesNamePluralDict[prevTriplesLevel] + ' '
      else:
        if tensOnesConnector != '':
          tensPart = generalTensDict[strNumber[xCounter]] + ' <item repeat="0-1">' + tensOnesConnector + '</item> ' + generalOnesDict[strNumber[xCounter+1]] + ' ' + triplesNamePluralDict[prevTriplesLevel] + ' '
        else:
          tensPart = generalTensDict[strNumber[xCounter]] + ' ' + generalOnesDict[strNumber[xCounter+1]] + ' ' + triplesNamePluralDict[prevTriplesLevel] + ' '
    else:
      tensPart = generalTensDict[strNumber[xCounter]] + ' ' + triplesNamePluralDict[prevTriplesLevel] + ' '

    locstringNumber = tensPart + prevlocstringNumber

  return xCounter, locstringNumber

def buildRegularTriples(strNumber, numLength, xCounter, hundredsSequenceDict, tripleOnesDict, generalOnesDict, generalTensDict, generalTeensDict, triplesLimitDict, triplesNameDict, triplesNamePluralDict, prevTriplesLevel, prevlocstringNumber, greaterTensConnector, tensOnesConnector, language):
  hundredsPart = ''
  tensPart = ''
  locstringNumber = prevlocstringNumber
  triplesLevel = prevTriplesLevel
  hundredsTensOnesPart = ''
  useSingleTriplesName = 0

  if numLength >= triplesLimitDict[prevTriplesLevel]:
    xCounter = xCounter - 3

    if strNumber[xCounter] != '0':
      hundredsPart = hundredsSequenceDict[strNumber[xCounter]]
      
      if strNumber[xCounter+1] != '0' and strNumber[xCounter+2] != '0':
        if strNumber[xCounter+1] == '1':
          tensPart = generalTeensDict[strNumber[xCounter+2]]
        else:
          if tensOnesConnector != '':
            tensPart = generalTensDict[strNumber[xCounter+1]] + ' <item repeat="0-1">' + tensOnesConnector + '</item> ' + generalOnesDict[strNumber[xCounter+2]]
          else:
            tensPart = generalTensDict[strNumber[xCounter+1]] + ' ' + generalOnesDict[strNumber[xCounter+2]]
      elif strNumber[xCounter+1] != '0' and strNumber[xCounter+2] == '0':
        tensPart = generalTensDict[strNumber[xCounter+1]]
      elif strNumber[xCounter+1] == '0' and strNumber[xCounter+2] != '0':
        tensPart = generalOnesDict[strNumber[xCounter+2]]
      elif strNumber[xCounter+1] == '0' and strNumber[xCounter+2] == '0':
        if strNumber[xCounter] == '1':
          hundredsPart = hundredsSequenceDict['0']
    else:
      if strNumber[xCounter+1] != '0' and strNumber[xCounter+2] != '0':
        if strNumber[xCounter+1] == '1':
          tensPart = generalTeensDict[strNumber[xCounter+2]]
        else:
          if tensOnesConnector != '':
            tensPart = generalTensDict[strNumber[xCounter+1]] + ' <item repeat="0-1">' + tensOnesConnector + '</item> ' + generalOnesDict[strNumber[xCounter+2]]
          else:
            tensPart = generalTensDict[strNumber[xCounter+1]] + ' ' + generalOnesDict[strNumber[xCounter+2]]
      elif strNumber[xCounter+1] != '0' and strNumber[xCounter+2] == '0':
        tensPart = generalTensDict[strNumber[xCounter+1]]
      elif strNumber[xCounter+1] == '0' and strNumber[xCounter+2] != '0':
        if strNumber[xCounter+2] == '1':
          useSingleTriplesName = 1
        tensPart = tripleOnesDict[strNumber[xCounter+2]]

    if hundredsPart != '' and tensPart != '':
      if tensPart != '':
        if greaterTensConnector != '':
          hundredsTensOnesPart = hundredsPart + ' <item repeat="0-1">' + greaterTensConnector + '</item> ' + tensPart + ' ' + triplesNamePluralDict[prevTriplesLevel] + ' '
        else:
          hundredsTensOnesPart = hundredsPart + ' ' + tensPart + ' ' + triplesNamePluralDict[prevTriplesLevel] + ' '
    elif hundredsPart != '':
      hundredsTensOnesPart = hundredsPart + ' ' + triplesNamePluralDict[prevTriplesLevel] + ' '
    elif tensPart != '':
      if useSingleTriplesName == 1:
        if greaterTensConnector != '':
          hundredsTensOnesPart = ' <item repeat="0-1">' + greaterTensConnector + '</item> ' + tensPart + ' ' + triplesNameDict[prevTriplesLevel] + ' '
        else:
          hundredsTensOnesPart = tensPart + ' ' + triplesNameDict[prevTriplesLevel] + ' '
      else:
        if greaterTensConnector != '':
          hundredsTensOnesPart = ' <item repeat="0-1">' + greaterTensConnector + '</item> ' + tensPart + ' ' + triplesNamePluralDict[prevTriplesLevel] + ' '
        else:
          hundredsTensOnesPart = tensPart + ' ' + triplesNamePluralDict[prevTriplesLevel] + ' '

    if hundredsPart != '' or tensPart != '':
      locstringNumber = hundredsTensOnesPart + prevlocstringNumber

    triplesLevel = triplesLevel + 1

  return xCounter, locstringNumber, triplesLevel

def checkVoiceNum(character, loclanguage):
  if character == '0':
    character = 'zero'

  if character == '1':
    character = 'one'

  if character == '2':
    character = 'two'

  if character == '3':
    character = 'three'

  if character == '4':
    character = 'four'

  if character == '5':
    character = 'five'

  if character == '6':
    character = 'six'

  if character == '7':
    character = 'seven'

  if character == '8':
    character = 'eight'

  if character == '9':
    character = 'nine'
	
  return character

def GetDTMFAlphaNumRetVal(character):
  retVal = ''
  if character == '0':
    retVal = '0'

  if character == '1':
    retVal = '1:.:_:@'

  if character == '2':
    retVal = '2:a:b:c'

  if character == '3':
    retVal = '3:d:e:f'

  if character == '4':
    retVal = '4:g:h:i'

  if character == '5':
    retVal = '5:j:k:l'

  if character == '6':
    retVal = '6:m:n:o'

  if character == '7':
    retVal = '7:p:q:r:s'

  if character == '8':
    retVal = '8:t:u:v'

  if character == '9':
    retVal = '9:w:x:y:z'

  return retVal

def GetDTMFAlphaOnlyRetVal(character):
  retVal = ''
  if character == '0' or character == '1':
    retVal = 'NOALPHA'

  if character == '2':
    retVal = 'a:b:c'

  if character == '3':
    retVal = 'd:e:f'

  if character == '4':
    retVal = 'g:h:i'

  if character == '5':
    retVal = 'j:k:l'

  if character == '6':
    retVal = 'm:n:o'

  if character == '7':
    retVal = 'p:q:r:s'

  if character == '8':
    retVal = 't:u:v'

  if character == '9':
    retVal = 'w:x:y:z'

  return retVal

def checkDTMFNum(character):
  retChar = ''
  if character == 'a' or character == 'b' or character == 'c':
    retChar = ' dtmf-2 '

  if character == 'd' or character == 'e' or character == 'f':
    retChar = ' dtmf-3 '

  if character == 'g' or character == 'h' or character == 'i':
    retChar = ' dtmf-4 '

  if character == 'j' or character == 'k' or character == 'l':
    retChar = ' dtmf-5 '

  if character == 'm' or character == 'n' or character == 'o':
    retChar = ' dtmf-6 '

  if character == 'p' or character == 'q' or character == 'r' or character == 's':
    retChar = ' dtmf-7 '

  if character == 't' or character == 'u' or character == 'v':
    retChar = ' dtmf-8 '

  if character == 'w' or character == 'x' or character == 'y' or character == 'z':
    retChar = ' dtmf-9 '

  if character == '0':
    retChar = ' dtmf-0 '

  if character == '1':
    retChar = ' dtmf-1 '

  if character == '2':
    retChar = ' dtmf-2 '

  if character == '3':
    retChar = ' dtmf-3 '

  if character == '4':
    retChar = ' dtmf-4 '

  if character == '5':
    retChar = ' dtmf-5 '

  if character == '6':
    retChar = ' dtmf-6 '

  if character == '7':
    retChar = ' dtmf-7 '

  if character == '8':
    retChar = ' dtmf-8 '

  if character == '9':
    retChar = ' dtmf-9 '
	
  if character == '@':
    retChar = ' dtmf-@ '
	
  if character == '*':
    retChar = ' dtmf-* '
	
  if character == '_':
    retChar = ' dtmf-_ '
	
  if character == '#':
    retChar = ' dtmf-# '
	
  if character == '.':
    retChar = ' dtmf-. '
	
  return retChar

def convertTuple(tup): 
  str =  ''.join(tup) 
  return str

def buildDecimal(decimalPart, numDecimal, generalSymbolsDict, generalOnesDict, generalDecimalNamesDict, addAltDecimals, language):
  locstringNumber = ''

  for locChar in decimalPart:
    locCharNum = generalOnesDict[locChar]
    locstringNumber = locstringNumber + ' ' + locCharNum

  locstringNumber = ' ' + generalSymbolsDict['.'] + locstringNumber

  if addAltDecimals == 1:
    numLength = len(decimalPart)
    addDecimalPart = numDecimal + ' ' + generalDecimalNamesDict[numLength]
    locstringNumber = '<one-of><item>' + locstringNumber + '</item><item>' + addDecimalPart + '</item></one-of>'

  return locstringNumber

def createNumGrammar(strNumber, tripleOnesDict, generalSymbolsDict, generalOnesDict, generalTensDict, generalTeensDict, triplesNameDict, triplesNamePluralDict, hundredsSequenceDict, hundredsTeensSequenceDict, thousandsSequenceDict, triplesLevel, triplesLimitDict, greaterTensConnector, tensOnesConnector, generalDecimalNamesDict, decimalConnector, language):

  thousandsHundredsPart = ''
  thousandsPart = ''
  hundredsPart = ''
  tensOnesPart = ''
  decimalPart = ''

  additionalHundredsPart = ''
  locstringNumber = ''

  if '.' in strNumber:
    numArray = strNumber.split('.')
    strNumber = numArray[0]
    decimalPart = numArray[1]

  numLength = len(strNumber)

  if 'es-' in language:
    if numLength <= 3:
      greaterTensConnector = ''

  xCounter = numLength-1

#Tens/Ones
  if numLength >= 1:
    tensOnesPart = generalOnesDict[strNumber[xCounter]]

  if numLength >= 2:
    xCounter = xCounter - 1
    if strNumber[xCounter] == '0':
      if strNumber[xCounter+1] == '0':
        tensOnesPart = ''
      else:
        tensOnesPart = generalOnesDict[strNumber[xCounter+1]]
    elif strNumber[xCounter] == '1':
      if strNumber[xCounter+1] == '0':
        tensOnesPart = generalTensDict[strNumber[xCounter]] + ' '
      else:
        tensOnesPart = generalTeensDict[strNumber[xCounter+1]]
    else:
      if strNumber[xCounter+1] == '0':
        tensOnesPart = generalTensDict[strNumber[xCounter]] + ' '
      else:
        if tensOnesConnector != '':
          tensOnesPart = generalTensDict[strNumber[xCounter]] + ' <item repeat="0-1">' + tensOnesConnector + '</item> ' + generalOnesDict[strNumber[xCounter+1]]
        else:
          tensOnesPart = generalTensDict[strNumber[xCounter]] + ' ' + generalOnesDict[strNumber[xCounter+1]]
    if numLength > 2:
      if tensOnesPart != '':
        if greaterTensConnector != '':
          tensOnesPart = ' <item repeat="0-1">' + greaterTensConnector + '</item> ' + tensOnesPart
        else:
          tensOnesPart = ' ' + tensOnesPart

  if tensOnesPart != '':
    locstringNumber = tensOnesPart

#Hundreds
  if numLength >= 3:
    xCounter = xCounter - 1
    if strNumber[xCounter] != '0':
      if strNumber[xCounter] == '1' and strNumber[xCounter+1] == '0' and strNumber[xCounter+2] == '0':
        hundredsPart = hundredsSequenceDict['0']
      else:
        hundredsPart = hundredsSequenceDict[strNumber[xCounter]]
      locstringNumber = hundredsPart + tensOnesPart
#    if numLength == 3:
#      thousandsHundredsPart = hundredsPart
#      locstringNumber = thousandsHundredsPart + tensOnesPart

#Thousands
  if numLength == 4:
    xCounter = xCounter - 1
    thousandsPart = thousandsSequenceDict[strNumber[xCounter]]
    thousandsHundredsPart = thousandsPart
    if hundredsPart != '':
      thousandsHundredsPart = thousandsPart + hundredsPart

    if 'en-' in language:
      if strNumber[xCounter+1] != '0':
        if strNumber[xCounter] == '1':
          additionalHundredsPart = hundredsTeensSequenceDict[strNumber[xCounter+1]]
        elif int(strNumber[xCounter]) > 1:
          additionalHundredsPart = generalTensDict[strNumber[xCounter]] + ' ' + hundredsSequenceDict[strNumber[xCounter+1]]

        thousandsHundredsPart = '<one-of><item>' + thousandsPart + hundredsPart + '</item><item>' + additionalHundredsPart + '</item></one-of>'

    locstringNumber = thousandsHundredsPart + tensOnesPart

#Ten Thousands
  xCounter, locstringNumber = buildRegularTens(strNumber, numLength, xCounter, tripleOnesDict, generalOnesDict, generalTensDict, generalTeensDict, 5, triplesNameDict, triplesNamePluralDict, 0, locstringNumber, tensOnesConnector, language)
  
#Hundred Thousands
  xCounter, locstringNumber, triplesLevel = buildRegularTriples(strNumber, numLength, xCounter, hundredsSequenceDict, tripleOnesDict, generalOnesDict, generalTensDict, generalTeensDict, triplesLimitDict, triplesNameDict, triplesNamePluralDict, triplesLevel, locstringNumber, greaterTensConnector, tensOnesConnector, language)

#Millions
  allowAlternate = 0
  prevActive = 0
  xCounter, locstringNumber, triplesLevel, prevActive = buildRegularMultiLevel(strNumber, numLength, xCounter, hundredsSequenceDict, tripleOnesDict, generalOnesDict, generalTensDict, generalTeensDict, triplesLimitDict, 7, triplesNameDict, triplesNamePluralDict, 1, triplesLevel, locstringNumber, greaterTensConnector, tensOnesConnector, language, allowAlternate, prevActive, thousandsSequenceDict)

  allowAlternate = 0
  if prevActive == 1:
    allowAlternate = 1

#Billions/Mil Milliones
  xCounter, locstringNumber, triplesLevel, prevActive = buildRegularMultiLevel(strNumber, numLength, xCounter, hundredsSequenceDict, tripleOnesDict, generalOnesDict, generalTensDict, generalTeensDict, triplesLimitDict, 10, triplesNameDict, triplesNamePluralDict, 2, triplesLevel, locstringNumber, greaterTensConnector, tensOnesConnector, language, allowAlternate, prevActive, thousandsSequenceDict)
  
  allowAlternate = 0
  if prevActive == 1:
    allowAlternate = 1

#Trillions/Billiones
  xCounter, locstringNumber, triplesLevel, prevActive = buildRegularMultiLevel(strNumber, numLength, xCounter, hundredsSequenceDict, tripleOnesDict, generalOnesDict, generalTensDict, generalTeensDict, triplesLimitDict, 13, triplesNameDict, triplesNamePluralDict, 3, triplesLevel, locstringNumber, greaterTensConnector, tensOnesConnector, language, allowAlternate, prevActive, thousandsSequenceDict)

  allowAlternate = 0
  if prevActive == 1:
    allowAlternate = 1

#			<item> a a a veinte <item repeat="0-1"> y </item> uno mil ciento  <item repeat="0-1"> y </item> siete mil billiones
#			<tag>Z0='aaa 21 T107 000 B000 000 M000 000'

# <item> a a a cero mil quinientos  <item repeat="0-1"> y </item> veinte <item repeat="0-1"> y </item> uno trilliones ciento  <item repeat="0-1"> y </item> siete mil billiones
#<tag>Z0='aaa 521 T107 000 B000 000 M000 000'</tag></item>

#Quadrillions/Mil Billiones
  xCounter, locstringNumber, triplesLevel, prevActive = buildRegularMultiLevel(strNumber, numLength, xCounter, hundredsSequenceDict, tripleOnesDict, generalOnesDict, generalTensDict, generalTeensDict, triplesLimitDict, 16, triplesNameDict, triplesNamePluralDict, 4, triplesLevel, locstringNumber, greaterTensConnector, tensOnesConnector, language, allowAlternate, prevActive, thousandsSequenceDict)

  allowAlternate = 0
  if prevActive == 1:
    allowAlternate = 1

#Quintillions/Trilliones
  xCounter, locstringNumber, triplesLevel, prevActive = buildRegularMultiLevel(strNumber, numLength, xCounter, hundredsSequenceDict, tripleOnesDict, generalOnesDict, generalTensDict, generalTeensDict, triplesLimitDict, 19, triplesNameDict, triplesNamePluralDict, 5, triplesLevel, locstringNumber, greaterTensConnector, tensOnesConnector, language, allowAlternate, prevActive, thousandsSequenceDict)

  allowAlternate = 0
  if prevActive == 1:
    allowAlternate = 1

#Sextillions/Mil Trilliones
  xCounter, locstringNumber, triplesLevel, prevActive = buildRegularMultiLevel(strNumber, numLength, xCounter, hundredsSequenceDict, tripleOnesDict, generalOnesDict, generalTensDict, generalTeensDict, triplesLimitDict, 22, triplesNameDict, triplesNamePluralDict, 6, triplesLevel, locstringNumber, greaterTensConnector, tensOnesConnector, language, allowAlternate, prevActive, thousandsSequenceDict)

  allowAlternate = 0
  if prevActive == 1:
    allowAlternate = 1

#Septillions/Quatrilliones
  xCounter, locstringNumber, triplesLevel, prevActive = buildRegularMultiLevel(strNumber, numLength, xCounter, hundredsSequenceDict, tripleOnesDict, generalOnesDict, generalTensDict, generalTeensDict, triplesLimitDict, 25, triplesNameDict, triplesNamePluralDict, 7, triplesLevel, locstringNumber, greaterTensConnector, tensOnesConnector, language, allowAlternate, prevActive, thousandsSequenceDict)

  allowAlternate = 0
  if prevActive == 1:
    allowAlternate = 1

#Octillions/Mil Quatrilliones
  xCounter, locstringNumber, triplesLevel, prevActive = buildRegularMultiLevel(strNumber, numLength, xCounter, hundredsSequenceDict, tripleOnesDict, generalOnesDict, generalTensDict, generalTeensDict, triplesLimitDict, 28, triplesNameDict, triplesNamePluralDict, 8, triplesLevel, locstringNumber, greaterTensConnector, tensOnesConnector, language, allowAlternate, prevActive, thousandsSequenceDict)

  if decimalPart != '':
    numDecimal = ''
    addAltDecimals = 1
    if addAltDecimals == 1:
      scanDecimal = decimalPart.lstrip('0')
      numDecimal = createNumGrammar(scanDecimal, tripleOnesDict, generalSymbolsDict, generalOnesDict, generalTensDict, generalTeensDict, triplesNameDict, triplesNamePluralDict, hundredsSequenceDict, hundredsTeensSequenceDict, thousandsSequenceDict, triplesLevel, triplesLimitDict, greaterTensConnector, tensOnesConnector, generalDecimalNamesDict, decimalConnector, language)
      numDecimal = decimalConnector + numDecimal

    locstringNumber = locstringNumber + buildDecimal(decimalPart, numDecimal, generalSymbolsDict, generalOnesDict, generalDecimalNamesDict, addAltDecimals, language)

  return locstringNumber

def multiSplit(delimiters, string, maxsplit=0):
  regexPattern = '|'.join(map(re.escape, delimiters))
  return re.split(regexPattern, string, maxsplit)

def replaceVoiceStatic(pattern, tripleOnesDict, generalSymbolsDict, generalOnesDict, generalTensDict, generalTeensDict, triplesNameDict, triplesNamePluralDict, hundredsSequenceDict, hundredsTeensSequenceDict, thousandsSequenceDict, triplesLevel, triplesLimitDict, greaterTensConnector, tensOnesConnector, generalDecimalNamesDict, prefabGrammars, prefabCollector, decimalConnector, language):
  buildPatval = ''
  defaultRetval = 'ZVAL'
  retval = ''
  changePattern = pattern
  removeChars = "(){}"
  replaceChars = "-_"
  locVals = {}

  for rChar in removeChars:
    changePattern = changePattern.replace(rChar,"")

  for locPattern in changePattern.split(' '):
    if '$$' in locPattern:
      locPattern = locPattern.replace('$',"")
      locVals = locPattern.split(':')
      retval = retval + '<item><ruleref uri="#' + prefabGrammars[locVals[0]] + '"/></item>'
      prefabCollector[prefabGrammars[locVals[0]]] = 1
    elif '$' in locPattern:
      locPattern = locPattern.replace('$',"")
      if ':' in locPattern:
        locVals = locPattern.split(':')
      else:
        locVals[0] = locPattern
        locVals[1] = defaultRetval

      prefabCollector[prefabGrammars[locVals[0]]] = 1

      retval = retval + '<item><ruleref uri="#' + prefabGrammars[locVals[0]] + '"/></item>'
      buildPatval = buildPatval + prefabGrammars[locVals[0]] + '.' + locVals[1]
    elif any(map(str.isalpha, locPattern)):
      for locChar in locPattern:
        if locChar != '(' and locChar != ')':
          if locChar.isalpha():
            retval = retval + ' ' + locChar
            buildPatval = buildPatval + locChar
          elif locChar == '-' or locChar == '_':
            retval = retval + ' ' + generalSymbolsDict[locChar] + ' '
            buildPatval = buildPatval + locChar
          else:
            locCharNum = generalOnesDict[locChar]
            retval = retval + ' ' + locCharNum
            buildPatval = buildPatval + locChar
    else:
# Handle dashes and underscore, e.g., 508-365
      if '-' in locPattern or '_' in locPattern:
        for rChar in replaceChars:
          if rChar == '-':
            locPattern = locPattern.replace(rChar,"-<dash>-")
          else:
            locPattern = locPattern.replace(rChar,"_<underscore>_")

        delimiters = ["-", "_"]
        for locSubPattern in multiSplit(delimiters, locPattern):
          if locSubPattern == '<dash>':
              retval = retval + ' ' + generalSymbolsDict['-'] + ' '
              buildPatval = buildPatval + '-'
          elif locSubPattern == '<underscore>':
              retval = retval + ' ' + generalSymbolsDict['_'] + ' '
              buildPatval = buildPatval + '_'
          elif locSubPattern[0] == '0':
            for locSubChar in locSubPattern:
              locSubCharNum = generalOnesDict[locSubChar]
              retval = retval + ' ' + locSubCharNum
              buildPatval = buildPatval + locSubChar
          else:
            locSubNum =  createNumGrammar(locSubPattern, tripleOnesDict, generalSymbolsDict, generalOnesDict, generalTensDict, generalTeensDict, triplesNameDict, triplesNamePluralDict, hundredsSequenceDict, hundredsTeensSequenceDict, thousandsSequenceDict, triplesLevel, triplesLimitDict, greaterTensConnector, tensOnesConnector, generalDecimalNamesDict, decimalConnector, language)
            retval = retval + ' ' + locSubNum
            buildPatval = buildPatval + locSubPattern
      else:
        if locPattern[0] == '0':
          for locChar in locPattern:
            locCharNum = generalOnesDict[locChar]
            retval = retval + ' ' + locCharNum
            buildPatval = buildPatval + locChar
        else:
          locNum =  createNumGrammar(locPattern, tripleOnesDict, generalSymbolsDict, generalOnesDict, generalTensDict, generalTeensDict, triplesNameDict, triplesNamePluralDict, hundredsSequenceDict, hundredsTeensSequenceDict, thousandsSequenceDict, triplesLevel, triplesLimitDict, greaterTensConnector, tensOnesConnector, generalDecimalNamesDict, decimalConnector, language)
          retval = retval + ' ' + locNum
          buildPatval = buildPatval + locPattern

  return retval, buildPatval

def replaceVoicePattern(pattern):
  retval = ''
  loopCnt = 0
  locStart = 0
  locEnd = 0
  locError = 0
  buildPatval = "none:ERROR"
  removeChars = "{}"
  changePattern = pattern

  for rChar in removeChars:
    changePattern = changePattern.replace(rChar,"")

  locp1 = re.compile(r'(\d+)')
  locIterator = locp1.finditer(pattern)
  for locMatch in locIterator:
    locg1 = locMatch.group()
    if locg1 is None:
      retval = retval + ' ' + pattern + ': POSSIBLE HTTP SYNTAX ERROR IN PATTERN'
      locError = 1
      break
    else:
      if loopCnt == 0:
        locStart = locg1
      else:
        locEnd = locg1
    loopCnt = loopCnt + 1

  if locError == 0:
    if '[sd' in pattern or '|sd' in pattern:
      if locEnd != 0:
        retval = '<ruleref uri="#GenSingleDigits' + locStart + '-' + locEnd + '"/>'
        buildPatval = 'GenSingleDigits' + locStart + '-' + locEnd
      else:
        retval = '<ruleref uri="#GenSingleDigits' + locStart + '"/>'
        buildPatval = 'GenSingleDigits' + locStart

    if '[xd' in pattern or '|xd' in pattern:
      if locEnd != 0:
        retval = '<ruleref uri="#GenExtendedDigits' + locStart + '-' + locEnd + '"/>'
        buildPatval = 'GenExtendedDigits' + locStart + '-' + locEnd
      else:
        retval = '<ruleref uri="#GenExtendedDigits' + locStart + '"/>'
        buildPatval = 'GenExtendedDigits' + locStart

    if '[sw' in pattern or '|sw' in pattern:
      if locEnd != 0:
        retval = '<ruleref uri="#GenSingleAlphaNum' + locStart + '-' + locEnd + '"/>'
        buildPatval = 'GenSingleAlphaNum' + locStart + '-' + locEnd
      else:
        retval = '<ruleref uri="#GenSingleAlphaNum' + locStart + '"/>'
        buildPatval = 'GenSingleAlphaNum' + locStart

    if '[xw' in pattern or '|xw' in pattern:
      if locEnd != 0:
        retval = '<ruleref uri="#GenExtendedAlphaNum' + locStart + '-' + locEnd + '"/>'
        buildPatval = 'GenExtendedAlphaNum' + locStart + '-' + locEnd
      else:
        retval = '<ruleref uri="#GenExtendedAlphaNum' + locStart + '"/>'
        buildPatval = 'GenExtendedAlphaNum' + locStart

    if '[sa' in pattern or '|sa' in pattern:
      if locEnd != 0:
        retval = '<ruleref uri="#GenSingleAlphaOnly' + locStart + '-' + locEnd + '"/>'
        buildPatval = 'GenSingleAlphaOnly' + locStart + '-' + locEnd
      else:
        retval = '<ruleref uri="#GenSingleAlphaOnly' + locStart + '"/>'
        buildPatval = 'GenSingleAlphaOnly' + locStart

    if '[xa' in pattern or '|xa' in pattern:
      if locEnd != 0:
        retval = '<ruleref uri="#GenExtendedAlphaOnly' + locStart + '-' + locEnd + '"/>'
        buildPatval = 'GenExtendedAlphaOnly' + locStart + '-' + locEnd
      else:
        retval = '<ruleref uri="#GenExtendedAlphaOnly' + locStart + '"/>'
        buildPatval = 'GenExtendedAlphaOnly' + locStart

  if buildPatval == "none:ERROR":
    buildPatval = pattern

  return retval, buildPatval, locStart, locEnd

# http://localhost:8000/api/gengrammar/run?required_type=alphanum&dtmf_limit=9&dtmf_retvals=1^wsx:2^edc:_hash_^hash:_star_^star&truth=[sd1-5]&dweight=0.02&dtmf=true&decoy=1,2&slot_name=WORD&language=en-US
def replaceDTMFStatic(pattern, language):
  buildPatval = ''
  retval = ''
  changePattern = pattern
  removeChars = "(){}"

  for rChar in removeChars:
    changePattern = changePattern.replace(rChar,"")

  for locPattern in changePattern.split(' '):
    for locChar in locPattern:
      retval = retval + ' ' + checkDTMFNum(locChar) + ' '
      buildPatval = buildPatval + locChar

  return retval, buildPatval

def replaceDTMFPattern(pattern):
  retval = ''
  loopCnt = 0
  locStart = 0
  locEnd = 0
  locError = 0
  buildPatval = "none:ERROR"
  removeChars = "{}"
  changePattern = pattern

  for rChar in removeChars:
    changePattern = changePattern.replace(rChar,"")

  locp1 = re.compile(r'(\d+)')
  locIterator = locp1.finditer(pattern)
  for locMatch in locIterator:
    locg1 = locMatch.group()
    if locg1 is None:
      retval = retval + ' ' + pattern + ': POSSIBLE HTTP SYNTAX ERROR IN PATTERN'
      locError = 1
      break
    else:
      if loopCnt == 0:
        locStart = locg1
      else:
        locEnd = locg1
    loopCnt = loopCnt + 1

  if locError == 0:
    if '[sd' in pattern or '|sd' in pattern:
      if locEnd != 0:
        retval = '<ruleref uri="#GenSingleDigits_DTMF' + locStart + '-' + locEnd + '"/>'
        buildPatval = 'GenSingleDigits_DTMF' + locStart + '-' + locEnd
      else:
        retval = '<ruleref uri="#GenSingleDigits_DTMF' + locStart + '"/>'
        buildPatval = 'GenSingleDigits_DTMF' + locStart

    if '[sw' in pattern or '|sw' in pattern:
      if locEnd != 0:
        retval = '<ruleref uri="#GenSingleAlphaNum_DTMF' + locStart + '-' + locEnd + '"/>'
        buildPatval = 'GenSingleAlphaNum_DTMF' + locStart + '-' + locEnd
      else:
        retval = '<ruleref uri="#GenSingleAlphaNum_DTMF' + locStart + '"/>'
        buildPatval = 'GenSingleAlphaNum_DTMF' + locStart

    if '[sa' in pattern or '|sa' in pattern:
      if locEnd != 0:
        retval = '<ruleref uri="#GenSingleAlphaOnly_DTMF' + locStart + '-' + locEnd + '"/>'
        buildPatval = 'GenSingleAlphaOnly_DTMF' + locStart + '-' + locEnd
      else:
        retval = '<ruleref uri="#GenSingleAlphaOnly_DTMF' + locStart + '"/>'
        buildPatval = 'GenSingleAlphaOnly_DTMF' + locStart

  if buildPatval == "none:ERROR":
    buildPatval = pattern

  return retval, buildPatval

def replaceAlphanum(request, locdtmf, loclanguage):
  requestChange = request
  buildstring = ''
  separator = ''
  if locdtmf == 'true':
    for locElem in list(requestChange):
      buildstring = buildstring+separator+checkDTMFNum(str(locElem))
      separator = ' '
  else:
    for locElem in list(requestChange):
      buildstring = buildstring+separator+checkVoiceNum(locElem, loclanguage)
      separator = ' '


  requestChange = buildstring
  
  return requestChange

def replacePattern(loctruth, locrequired_type, locdtmf, addGrammarDict_DTMF, addGrammarDict, tripleOnesDict, generalSymbolsDict, generalOnesDict, generalTensDict, generalTeensDict, triplesNameDict, triplesNamePluralDict, hundredsSequenceDict, hundredsTeensSequenceDict, thousandsSequenceDict, triplesLevel, triplesLimitDict, greaterTensConnector, tensOnesConnector, generalDecimalNamesDict, prefabGrammars, prefabCollector, decimalConnector, language):
  locbuildtruth = ''
  locnewline = ''
  locbuildretval = ''
  locSeparator = ''
  staticCounter = 0

  p1 = re.compile(r'(\{{0,1})(((\[((sa|xa|sd|xd|sw|xw)(\d+)(-(\d+)){0,1})\]))|(\[(((sa|xa|sd|xd|sw|xw)(\d+)(-(\d+)){0,1})|\|)+\])|(\(((\_|\-|\||\$|\s|\.|\:|\d|\w)+)\))|(\(\$(\||(\_|\-|\d|\w)+)\))|(\$((\_|\-|\d|\w)+)))(\}{0,1})')

  if locdtmf == 'true':
    iterator = p1.finditer(loctruth)
    for match in iterator:
      itemStart = '<item>'
      if '{' in match.group():
        itemStart = '<item repeat="0-1">'

      if '[' in match.group() and '|' not in match.group():
        repg, buildg = replaceDTMFPattern(match.group())
        addGrammarDict_DTMF[buildg] = 1
        locbuildtruth = locbuildtruth + '\n\t\t\t' + itemStart + repg + '</item>'
        locbuildretval = locbuildretval + locSeparator + buildg + '.PATVAL'
        locSeparator = ' + '
      elif '[' in match.group() and '|' in match.group():
        locbuildtruth = locbuildtruth + '\n\t\t\t' + itemStart + '\n\t\t\t\t' + '<one-of>'
        for locPattern in match.group().split('|'):
          locPattern = '|' + locPattern
          repg, buildg = replaceDTMFPattern(locPattern)
          addGrammarDict_DTMF[buildg] = 1
          locbuildtruth = locbuildtruth + '\n\t\t\t\t\t<item>' + repg + '<tag>Z' + str(staticCounter) + "='" + buildg + '.PATVAL' + '</tag>' + '</item>'
          locSeparator = ' + '

        if locbuildretval != '':
          locbuildretval = locbuildretval + locSeparator + 'Z' + str(staticCounter)
        else:
          locbuildretval = 'Z' + str(staticCounter)

        locbuildtruth = locbuildtruth + '\n\t\t\t\t' + '</one-of>' + '\n\t\t\t</item>'
        staticCounter = staticCounter + 1
      elif '(' in match.group() and '|' not in match.group():
        repg, buildg = replaceDTMFStatic(match.group(), language)
        if buildg != '':
          locbuildtruth = locbuildtruth + '\n\t\t\t' + itemStart + repg + '<tag>Z' + str(staticCounter) + "='" + buildg + "'</tag></item>"
          locbuildretval = locbuildretval + locSeparator + 'Z' + str(staticCounter)
          locSeparator = ' + '
          staticCounter = staticCounter + 1
        else:
          locbuildtruth = locbuildtruth + '\n\t\t\t' + itemStart + repg + '</item>'

      elif '(' in match.group() and '|' in match.group():
        locbuildtruth = locbuildtruth + '\n\t\t\t' + itemStart + '\n\t\t\t\t' + '<one-of>'
        for locPattern in match.group().split('|'):
          repg, buildg = replaceDTMFStatic(locPattern, language)
          if buildg != '':
            locbuildtruth = locbuildtruth + '\n\t\t\t\t\t<item>' + repg + '<tag>Z' + str(staticCounter) + "='" + buildg + '"</tag>' + '</item>'
            locSeparator = ' + '
          else:
            locbuildtruth = locbuildtruth + '\n\t\t\t\t\t<item>' + repg + '</item>'

        if locbuildretval != '':
          locbuildretval = locbuildretval + locSeparator + 'Z' + str(staticCounter)
        else:
          locbuildretval = 'Z' + str(staticCounter)
        staticCounter = staticCounter + 1

        locbuildtruth = locbuildtruth + '\n\t\t\t\t' + '</one-of>' + '\n\t\t\t</item>'
  else:
    iterator = p1.finditer(loctruth)
    for match in iterator:
      itemStart = '<item>'
      if '{' in match.group():
        itemStart = '<item repeat="0-1">'

      if '[' in match.group() and '|' not in match.group():
        repg, buildg, locStart, locEnd = replaceVoicePattern(match.group())
        addGrammarDict[buildg] = str(locStart) + ':' + str(locEnd)
        locbuildtruth = locbuildtruth + '\n\t\t\t' + itemStart + repg + '</item>'
        locbuildretval = locbuildretval + locSeparator + buildg + '.PATVAL'
        locSeparator = ' + '
      elif '[' in match.group() and '|' in match.group():
        locbuildtruth = locbuildtruth + '\n\t\t\t' + itemStart + '\n\t\t\t\t' + '<one-of>'
        for locPattern in match.group().split('|'):
          locPattern = '|' + locPattern
          repg, buildg, locStart, locEnd = replaceVoicePattern(locPattern)
          addGrammarDict[buildg] = str(locStart) + ':' + str(locEnd)
          locbuildtruth = locbuildtruth + '\n\t\t\t\t\t<item>' + repg + '<tag>Z' + str(staticCounter) + "='" + buildg + '.PATVAL' + '</tag>' + '</item>'
          locSeparator = ' + '

        if locbuildretval != '':
          locbuildretval = locbuildretval + locSeparator + 'Z' + str(staticCounter)
        else:
          locbuildretval = 'Z' + str(staticCounter)

        locbuildtruth = locbuildtruth + '\n\t\t\t\t' + '</one-of>' + '\n\t\t\t</item>'
        staticCounter = staticCounter + 1
      elif '(' in match.group() and '|' not in match.group():
        repg, buildg = replaceVoiceStatic(match.group(), tripleOnesDict, generalSymbolsDict, generalOnesDict, generalTensDict, generalTeensDict, triplesNameDict, triplesNamePluralDict, hundredsSequenceDict, hundredsTeensSequenceDict, thousandsSequenceDict, triplesLevel, triplesLimitDict, greaterTensConnector, tensOnesConnector, generalDecimalNamesDict, prefabGrammars, prefabCollector, decimalConnector, language)
        if buildg != '':
          locbuildtruth = locbuildtruth + '\n\t\t\t' + itemStart + repg + '<tag>Z' + str(staticCounter) + "='" + buildg + "'</tag></item>"
          locbuildretval = locbuildretval + locSeparator + 'Z' + str(staticCounter)
          locSeparator = ' + '
          staticCounter = staticCounter + 1
        else:
          locbuildtruth = locbuildtruth + '\n\t\t\t' + itemStart + repg + '</item>'

      elif '(' in match.group() and '|' in match.group():
        locbuildtruth = locbuildtruth + '\n\t\t\t' + itemStart + '\n\t\t\t\t' + '<one-of>'
        for locPattern in match.group().split('|'):
          repg, buildg = replaceVoiceStatic(locPattern, tripleOnesDict, generalSymbolsDict, generalOnesDict, generalTensDict, generalTeensDict, triplesNameDict, triplesNamePluralDict, hundredsSequenceDict, hundredsTeensSequenceDict, thousandsSequenceDict, triplesLevel, triplesLimitDict, greaterTensConnector, tensOnesConnector, generalDecimalNamesDict, prefabGrammars, prefabCollector, decimalConnector, language)
          if buildg != '':
            locbuildtruth = locbuildtruth + '\n\t\t\t\t\t<item>' + repg + '<tag>Z' + str(staticCounter) + "='" + buildg + '"</tag>' + '</item>'
            locSeparator = ' + '
          else:
            locbuildtruth = locbuildtruth + '\n\t\t\t\t\t<item>' + repg + '</item>'

        if locbuildretval != '':
          locbuildretval = locbuildretval + locSeparator + 'Z' + str(staticCounter)
        else:
          locbuildretval = 'Z' + str(staticCounter)
        staticCounter = staticCounter + 1

        locbuildtruth = locbuildtruth + '\n\t\t\t\t' + '</one-of>' + '\n\t\t\t</item>'

  locbuildtruth = '<item>' + locbuildtruth + '\n\t\t\t' + '<tag>RETVAL=' + locbuildretval + '</tag>' + '\n\t\t' + '</item>'

  return locbuildtruth

def createVoiceGrammar(grammarName, grammarType):
  secondary_loop = ''
  if grammarType == 'VoiceExtendedDigits':
    secondary_loop = 'VoiceExtendedDigits'
    grammarType = 'VoiceSingleDigits'
  elif grammarType == 'VoiceExtendedAlphaNum':
    secondary_loop = 'VoiceExtendedAlphaNum'
    grammarType = 'VoiceSingleAlphaNum'
  elif grammarType == 'VoiceExtendedAlphaOnly':
    secondary_loop = 'VoiceExtendedAlphaOnly'
    grammarType = 'VoiceSingleAlphaOnly'

  loopCnt = 0
  locp1 = re.compile(r'(\d+)')
  locIterator = locp1.finditer(grammarName)
  locEnd = -1
  holdLocEnd = locEnd
  for locMatch in locIterator:
    locg1 = locMatch.group()
    if locg1 is None:
      retval = retval + ' ' + grammarName + ': POSSIBLE HTTP SYNTAX ERROR IN PATTERN'
      locError = 1
      break
    else:
      if loopCnt == 0:
        locStart = int(locg1)
        holdLocStart = locStart
      else:
        locEnd = int(locg1)
        holdLocEnd = locEnd
    loopCnt = loopCnt + 1

  locGrammarBuildList = '\n\t<rule id="' + grammarName + '>' + '"\n\t<one-of>'
  
  if locEnd == -1:
    locEnd = locStart
    locStart = 0
	
    locGrammarBuildList = locGrammarBuildList + '\n\t\t<item>'
    for x in range(locStart, locEnd):
      locGrammarBuildList = locGrammarBuildList + '\n\t\t\t<item><ruleref uri="#' + grammarType + '"/><tag>Z' + str(x) + '=' + grammarType + '.ZVAL</tag></item>'

    locGrammarBuildList = locGrammarBuildList + '"\n\t\t\t<tag>PATVAL='
    for x in range(locStart, locEnd):
      if x == locStart:
        locGrammarBuildList = locGrammarBuildList + ' Z' + str(x)
      else:
        locGrammarBuildList = locGrammarBuildList + ' + Z' + str(x)

    locGrammarBuildList = locGrammarBuildList + '</tag>\n\t\t</item>'
  else:
    locStart = locStart - 1

    for y in range(locStart, locEnd):
      locGrammarBuildList = locGrammarBuildList + '\n\t\t<item>'
      for x in range(locStart, y+1):
        locGrammarBuildList = locGrammarBuildList + '\n\t\t\t<item><ruleref uri="#' + grammarType + '"/><tag>Z' + str(x) + '=' + grammarType + '.ZVAL</tag></item>'

      locGrammarBuildList = locGrammarBuildList + '"\n\t\t\t<tag>PATVAL='
      for x in range(locStart, y+1):
        if x == locStart:
          locGrammarBuildList = locGrammarBuildList + ' Z' + str(x)
        else:
          locGrammarBuildList = locGrammarBuildList + ' + Z' + str(x)

      locGrammarBuildList = locGrammarBuildList + '</tag>\n\t\t</item>'

  if secondary_loop != '':
    locStart = holdLocStart
    locEnd = holdLocEnd
    grammarType = secondary_loop
    if locEnd == -1:
      locGrammarBuildList = locGrammarBuildList + '\n\t\t<item>'
      locGrammarBuildList = locGrammarBuildList + '\n\t\t\t<item><ruleref uri="#' + grammarType + str(locStart) + '"/><tag>Z0=' + grammarType + str(locStart) + '.ZVAL</tag></item>'
      locGrammarBuildList = locGrammarBuildList + '"\n\t\t\t<tag>PATVAL=Z0</tag>\n\t\t</item>'
    else:
      locStart = locStart - 1

      for y in range(locStart, locEnd):
        if y > 0:
          locGrammarBuildList = locGrammarBuildList + '\n\t\t<item>'
          locGrammarBuildList = locGrammarBuildList + '\n\t\t\t<item><ruleref uri="#' + grammarType + str(y+1) + '"/><tag>Z0=' + grammarType + str(y+1) + '.ZVAL</tag></item>'
          locGrammarBuildList = locGrammarBuildList + '"\n\t\t\t<tag>PATVAL=Z0</tag>\n\t\t</item>'

  locGrammarBuildList = locGrammarBuildList + '"\n\t</one-of>\n\t</rule>'

  return locGrammarBuildList
  
def char_range(c1, c2):
# Generates the characters from `c1` to `c2`, inclusive."""
  for c in range(ord(c1), ord(c2)+1):
    yield chr(c)

def createVoiceSingleDigitsGrammar(grammarName, generalOnesDict, language):
  locGrammarBuildList = '\n\t<rule id="' + grammarName + '>' + '"\n\t<one-of>'
  if "en-" in language:
    locGrammarBuildList = locGrammarBuildList + '\n\t\t<item weight="0.3"' + ">oh <tag>  ZVAL='0'; </item>"
  for locnum in range(0, 10):
    locGrammarBuildList = locGrammarBuildList + "\n\t\t<item>" + generalOnesDict[str(locnum)] + "<tag>  ZVAL='" + str(locnum) + "'; </item>"

  locGrammarBuildList = locGrammarBuildList + '"\n\t</one-of>\n\t</rule>'
  return locGrammarBuildList

def createVoiceExtendedDigitsGrammar(grammarName, generalOnesDict, numRange, language):
  locSeparator = ''
  staticCounter = 0
  (locStart, locEnd) = numRange.split(':')
  if locEnd != '0':
    numRange = numRange.replace(':', '-')
  else:
    numRange = locStart
  locGrammarBuildList = '\n\t<rule id="' + grammarName + numRange + '>' + '"\n\t<one-of>'
#  singleGrammarName = grammarName.replace('Extended', 'Single')
  locStart = int(locStart)
  locEnd = int(locEnd)
  if locEnd == 0:
#	<rule id="VoiceExtendedDigits6>"
#	<one-of>
#		<item>
#           <item><ruleref uri="#doubleNum"/><tag>Z0=doubleNum.rVAL</tag></item>
#           <item><ruleref uri="#doubleNum"/><tag>Z1=doubleNum.rVAL</tag></item>
#           <item><ruleref uri="#doubleNum"/><tag>Z2=doubleNum.rVAL</tag></item>
#           <tag>ZVAL=Z0 + Z1 + Z2</tag>
#       </item>
#		<item>
#		    <item><ruleref uri="#tripleNum"/><tag>Z0=tripleNum.rVAL</tag></item>
#		    <item><ruleref uri="#tripleNum"/><tag>Z1=tripleNum.rVAL</tag></item>"
#           <tag>ZVAL=Z0 + Z1</tag>
#       </item>
#	</one-of>
#	</rule>

    modStart2 = locStart % 2
    modStart3 = locStart % 3
    if modStart2 == 0 and modStart3 == 0:
      locbuildretval = ''
      locGrammarBuildList = locGrammarBuildList + '\n\t\t<item>'
      for locincrem in range(0, int(locStart/2)):
        locGrammarBuildList = locGrammarBuildList + '\n\t\t\t<item><ruleref uri="#doubleNum"/><tag>Z' + str(locincrem) + '=doubleNum.rVAL</tag></item>'
        locbuildretval = locbuildretval + locSeparator + 'Z' + str(locincrem)
        locSeparator = ' + '
#        staticCounter = staticCounter + 1
      locGrammarBuildList = locGrammarBuildList + '\n\t\t\t<tag>ZVAL=' + locbuildretval + '</tag>'
      locGrammarBuildList = locGrammarBuildList + '\n\t\t</item>'

      locbuildretval = ''
      locGrammarBuildList = locGrammarBuildList + '\n\t\t<item>'
      for locincrem in range(0, int(locStart/3)):
        locGrammarBuildList = locGrammarBuildList + '\n\t\t\t<item><ruleref uri="#tripleNum"/><tag>Z' + str(locincrem) + '=tripleNum.rVAL</tag></item>'
        locbuildretval = locbuildretval + locSeparator + 'Z' + str(locincrem)
        locSeparator = ' + '
#        staticCounter = staticCounter + 1
      locGrammarBuildList = locGrammarBuildList + '\n\t\t\t<tag>ZVAL=' + locbuildretval + '</tag>'
      locGrammarBuildList = locGrammarBuildList + '\n\t\t</item>'
    elif modStart2 == 0:
      locbuildretval = ''
      locGrammarBuildList = locGrammarBuildList + '\n\t\t<item>'
      for locincrem in range(0, int(locStart/2)):
        locGrammarBuildList = locGrammarBuildList + '\n\t\t\t<item><ruleref uri="#doubleNum"/><tag>Z' + str(staticCounter) + '=doubleNum.rVAL</tag></item>'
        locbuildretval = locbuildretval + locSeparator + 'Z' + str(staticCounter)
        locSeparator = ' + '
        staticCounter = staticCounter + 1
      locGrammarBuildList = locGrammarBuildList + '\n\t\t\t<tag>ZVAL=' + locbuildretval + '</tag>'
      locGrammarBuildList = locGrammarBuildList + '\n\t\t</item>'
    elif modStart3 == 0:
      locbuildretval = ''
      locGrammarBuildList = locGrammarBuildList + '\n\t\t<item>'
      for locincrem in range(0, int(locStart/3)):
        locGrammarBuildList = locGrammarBuildList + '\n\t\t\t<item><ruleref uri="#tripleNum"/><tag>Z' + str(staticCounter) + '=tripleNum.rVAL</tag></item>'
        locbuildretval = locbuildretval + locSeparator + 'Z' + str(staticCounter)
        locSeparator = ' + '
        staticCounter = staticCounter + 1
      locGrammarBuildList = locGrammarBuildList + '\n\t\t\t<tag>ZVAL=' + locbuildretval + '</tag>'
      locGrammarBuildList = locGrammarBuildList + '\n\t\t</item>'
    else:
      kkkk
#    locGrammarBuildList = locGrammarBuildList + '\n\t\t\t<tag>ZVAL=' + locbuildretval + '</tag>'
#    locGrammarBuildList = locGrammarBuildList + '\n\t\t</item>'
  else:
    aaa = 1

  locGrammarBuildList = locGrammarBuildList + '"\n\t</one-of>\n\t</rule>'
  return locGrammarBuildList

def createVoiceSingleAlphaNumGrammar(grammarName, generalOnesDict, language):
  locGrammarBuildList = '\n\t<rule id="' + grammarName + '>' + '"\n\t<one-of>'
  if "en-" in language:
    locGrammarBuildList = locGrammarBuildList + '\n\t\t<item weight="0.3"' + ">oh <tag>  ZVAL='0'; </item>"
  for locnum in range(0, 10):
    locGrammarBuildList = locGrammarBuildList + "\n\t\t<item>" + generalOnesDict[str(locnum)] + "<tag>  ZVAL='" + str(locnum) + "'; </item>"

  for localpha in char_range('a', 'z'):
    locGrammarBuildList = locGrammarBuildList + "\n\t\t<item>" + localpha + "<tag>  ZVAL='" + localpha + "'; </item>"

  locGrammarBuildList = locGrammarBuildList + '"\n\t</one-of>\n\t</rule>'
  return locGrammarBuildList

def createVoiceSingleAlphaOnlyGrammar(grammarName, language):
  locGrammarBuildList = '\n\t<rule id="' + grammarName + '>' + '"\n\t<one-of>'
  for localpha in char_range('a', 'z'):
    locGrammarBuildList = locGrammarBuildList + "\n\t\t<item>" + localpha + "<tag>  ZVAL='" + localpha + "'; </item>"

  locGrammarBuildList = locGrammarBuildList + '"\n\t</one-of>\n\t</rule>'
  return locGrammarBuildList

def createDTMFGrammar(grammarName, grammarType):
  secondary_loop = ''
  if grammarType == 'DTMFExtendedDigits':
    secondary_loop = 'DTMFExtendedDigits'
    grammarType = 'DTMFSingleDigits'
  elif grammarType == 'DTMFExtendedAlphaNum':
    secondary_loop = 'DTMFExtendedAlphaNum'
    grammarType = 'DTMFSingleAlphaNum'
  elif grammarType == 'DTMFExtendedAlphaOnly':
    secondary_loop = 'DTMFExtendedAlphaOnly'
    grammarType = 'DTMFSingleAlphaOnly'

  loopCnt = 0
  locp1 = re.compile(r'(\d+)')
  locIterator = locp1.finditer(grammarName)
  locEnd = -1
  holdLocEnd = locEnd
  for locMatch in locIterator:
    locg1 = locMatch.group()
    if locg1 is None:
      retval = retval + ' ' + grammarName + ': POSSIBLE HTTP SYNTAX ERROR IN PATTERN'
      locError = 1
      break
    else:
      if loopCnt == 0:
        locStart = int(locg1)
        holdLocStart = locStart
      else:
        locEnd = int(locg1)
        holdLocEnd = locEnd
    loopCnt = loopCnt + 1

  locGrammarBuildList = '\n\t<rule id="' + grammarName + '>' + '"\n\t<one-of>'
  
  if locEnd == -1:
    locEnd = locStart
    locStart = 0
	
    locGrammarBuildList = locGrammarBuildList + '\n\t\t<item>'
    for x in range(locStart, locEnd):
      locGrammarBuildList = locGrammarBuildList + '\n\t\t\t<item><ruleref uri="#' + grammarType + '"/><tag>Z' + str(x) + '=' + grammarType + '.ZVAL</tag></item>'

    locGrammarBuildList = locGrammarBuildList + '"\n\t\t\t<tag>PATVAL='
    for x in range(locStart, locEnd):
      if x == locStart:
        locGrammarBuildList = locGrammarBuildList + ' Z' + str(x)
      else:
        locGrammarBuildList = locGrammarBuildList + ' + Z' + str(x)

    locGrammarBuildList = locGrammarBuildList + '</tag>\n\t\t</item>'
  else:
    locStart = locStart - 1

    for y in range(locStart, locEnd):
      locGrammarBuildList = locGrammarBuildList + '\n\t\t<item>'
      for x in range(locStart, y+1):
        locGrammarBuildList = locGrammarBuildList + '\n\t\t\t<item><ruleref uri="#' + grammarType + '"/><tag>Z' + str(x) + '=' + grammarType + '.ZVAL</tag></item>'

      locGrammarBuildList = locGrammarBuildList + '"\n\t\t\t<tag>PATVAL='
      for x in range(locStart, y+1):
        if x == locStart:
          locGrammarBuildList = locGrammarBuildList + ' Z' + str(x)
        else:
          locGrammarBuildList = locGrammarBuildList + ' + Z' + str(x)

      locGrammarBuildList = locGrammarBuildList + '</tag>\n\t\t</item>'

  if secondary_loop != '':
    locStart = holdLocStart
    locEnd = holdLocEnd
    grammarType = secondary_loop
    if locEnd == -1:
      locGrammarBuildList = locGrammarBuildList + '\n\t\t<item>'
      locGrammarBuildList = locGrammarBuildList + '\n\t\t\t<item><ruleref uri="#' + grammarType + str(locStart) + '"/><tag>Z0=' + grammarType + str(locStart) + '.ZVAL</tag></item>'
      locGrammarBuildList = locGrammarBuildList + '"\n\t\t\t<tag>PATVAL=Z0</tag>\n\t\t</item>'
    else:
      locStart = locStart - 1

      for y in range(locStart, locEnd):
        if y > 0:
          locGrammarBuildList = locGrammarBuildList + '\n\t\t<item>'
          locGrammarBuildList = locGrammarBuildList + '\n\t\t\t<item><ruleref uri="#' + grammarType + str(y+1) + '"/><tag>Z0=' + grammarType + str(y+1) + '.ZVAL</tag></item>'
          locGrammarBuildList = locGrammarBuildList + '"\n\t\t\t<tag>PATVAL=Z0</tag>\n\t\t</item>'

  locGrammarBuildList = locGrammarBuildList + '"\n\t</one-of>\n\t</rule>'

  return locGrammarBuildList
  
def createDTMFSingleDigitsGrammar(grammarName, dtmfNumRetvalDict, dtmfSymbolRetvalDict, dtmf_limit, loclanguage):
  locGrammarBuildList = '\n\t<rule id="' + grammarName + '>' + '"\n\t<one-of>'
  
  for locnum in range(0, dtmf_limit+1):
    locGrammarBuildList = locGrammarBuildList + "\n\t\t<item> dtmf-" + str(locnum) + "<tag>  ZVAL='" + dtmfNumRetvalDict[locnum] + "'; </item>"

  for locsym in dtmfSymbolRetvalDict:
    locGrammarBuildList = locGrammarBuildList + "\n\t\t<item> dtmf-" + locsym + "<tag>  ZVAL='" + dtmfSymbolRetvalDict[locsym] + "'; </item>"

  locGrammarBuildList = locGrammarBuildList + '"\n\t</one-of>\n\t</rule>'
  return locGrammarBuildList

def createDTMFSingleAlphaNumGrammar(grammarName, loclanguage):
  locGrammarBuildList = '\n\t<rule id="' + grammarName + '>' + '"\n\t<one-of>'

  for locnum in range(0, 10):
    locGrammarBuildList = locGrammarBuildList + "\n\t\t<item>" + checkDTMFNum(str(locnum)) + "<tag>  ZVAL='" + GetDTMFAlphaNumRetVal(str(locnum)) + "'; </item>"

#  for localpha in char_range('a', 'z'):
#    locGrammarBuildList = locGrammarBuildList + "\n\t\t<item>" + checkDTMFNum(localpha) + "<tag>  ZVAL='" + localpha + "'; </item>"

  locGrammarBuildList = locGrammarBuildList + '"\n\t</one-of>\n\t</rule>'
  return locGrammarBuildList

def createDTMFSingleAlphaOnlyGrammar(grammarName, loclanguage):
  locGrammarBuildList = '\n\t<rule id="' + grammarName + '>' + '"\n\t<one-of>'

  for locnum in range(0, 10):
    locGrammarBuildList = locGrammarBuildList + "\n\t\t<item>" + checkDTMFNum(str(locnum)) + "<tag>  ZVAL='" + GetDTMFAlphaOnlyRetVal(str(locnum)) + "'; </item>"

  locGrammarBuildList = locGrammarBuildList + '"\n\t</one-of>\n\t</rule>'
  return locGrammarBuildList

def gengrammar(request):
  validator, errors = method_validator(info=gengrammar_info, request=request)
  extractor = method_extractor(info=optional_gengrammar_info, request=request)

  default_mode = 'voice'
  default_weight = '0.99'
  default_dweight = '0.01'
  default_slot_name = 'choice'
  default_dtmf = 'false'
  default_dtmf_limit = 9
  default_language = 'en-GB'
  default_decoy = None

  dtmf_return_values_array = []
  required_type = validator('required_type')
  truth = validator('truth')

  decoy = extractor('decoy')
  dweight = extractor('dweight')
  slot_name = extractor('slot_name')
  weight = extractor('weight')
  dtmf = extractor('dtmf')
  dtmf_limit = extractor('dtmf_limit')
  if dtmf_limit is not None:
    dtmf_limit = int(dtmf_limit)
  dtmf_return_values = extractor('dtmf_retvals')
  language = extractor('language')

  if dtmf is None:
    dtmf = default_dtmf

  if dtmf_limit is None:
    dtmf_limit = default_dtmf_limit

  if dweight is None:
    dweight = default_dweight

  if slot_name is None:
    slot_name = default_slot_name

  if dtmf_return_values is not None:
    dtmf_return_values_array = dtmf_return_values.split(':')

  decoyTopRule = '\t\t<item weight="' + dweight + '">\n\t\t\t<item>\n\t\t\t\t<ruleref uri="#decoyITEMS"/>\n\t\t\t\t<tag>"' + slot_name + '"=decoyITEMS.RETVAL</tag>\n\t\t\t</item>\n\t\t</item>'

  if decoy is None:
    decoyTopRule = ""

  if language is None:
    language = default_language

  buildtruth = ''
  newline = ''
  addGrammars = 0
  addGrammarDict_DTMF = {}
  addGrammarDict = {}
  addGrammarDictLower = {}
  prefabGrammars = {}
  dtmfNumRetvalDict = {}
  dtmfSymbolRetvalDict = {}

  generalSymbolsDict = {}
  generalDTMFSymbolsDict = {}
  generalOnesDict = {}
  generalTensDict = {}
  generalTeensDict = {}
  triplesNameDict = {}
  triplesNamePluralDict = {}
  hundredsSequenceDict = {}
  hundredsTeensSequenceDict = {}
  thousandsSequenceDict = {}
  triplesLimitDict = {}
  tripleOnesDict = {}
  generalDecimalNamesDict = {}
  prefabGrammarstoGen = {}

  triplesLimitDict[0] = 6
  triplesLimitDict[1] = 9
  triplesLimitDict[2] = 12
  triplesLimitDict[3] = 15
  triplesLimitDict[4] = 18
  triplesLimitDict[5] = 21
  triplesLimitDict[6] = 24
  triplesLimitDict[7] = 27
  triplesLimitDict[8] = 30

  triplesLevel = 0

  prefabGrammars['yesnosimple'] = 'YESNO_SIMPLE'
  prefabGrammars['yesnoexpanded'] = 'YESNO_EXPANDED'
  prefabGrammars['hmwse'] = 'HMWSE'
  prefabGrammars['universals'] = 'UNIVERSALS'
  prefabGrammars['thanks'] = 'THANKS'
  prefabGrammars['uhum'] = 'UHUM'
  prefabGrammars['please'] = 'PLEASE'

  generalDTMFSymbolsDict['_hash_'] = '#'
  generalDTMFSymbolsDict['_star_'] = '*'

  if 'en-' in language:
    greaterTensConnector = ' and '
    tensOnesConnector = ''
    triplesNameDict[0] = 'thousand'
    triplesNameDict[1] = 'million'
    triplesNameDict[2] = 'billion'
    triplesNameDict[3] = 'trillion'
    triplesNameDict[4] = 'quadrillion'
    triplesNameDict[5] = 'quintillion'
    triplesNameDict[6] = 'sextillion'
    triplesNameDict[7] = 'septillion'
    triplesNameDict[8] = 'octillion'
  
    triplesNamePluralDict[0] = 'thousand'
    triplesNamePluralDict[1] = 'million'
    triplesNamePluralDict[2] = 'billion'
    triplesNamePluralDict[3] = 'trillion'
    triplesNamePluralDict[4] = 'quadrillion'
    triplesNamePluralDict[5] = 'quintillion'
    triplesNamePluralDict[6] = 'sextillion'
    triplesNamePluralDict[7] = 'septillion'
    triplesNamePluralDict[8] = 'octillion'
  
    hundredsSequenceDict['0'] = 'one hundred '
    hundredsSequenceDict['1'] = 'one hundred '
    hundredsSequenceDict['2'] = 'two hundred '
    hundredsSequenceDict['3'] = 'three hundred '
    hundredsSequenceDict['4'] = 'four hundred '
    hundredsSequenceDict['5'] = 'five hundred '
    hundredsSequenceDict['6'] = 'six hundred '
    hundredsSequenceDict['7'] = 'seven hundred '
    hundredsSequenceDict['8'] = 'eight hundred '
    hundredsSequenceDict['9'] = 'nine hundred '

    hundredsTeensSequenceDict['1'] = 'eleven hundred '
    hundredsTeensSequenceDict['2'] = 'twelve hundred '
    hundredsTeensSequenceDict['3'] = 'thirteen hundred '
    hundredsTeensSequenceDict['4'] = 'fourteen hundred '
    hundredsTeensSequenceDict['5'] = 'fifteen hundred '
    hundredsTeensSequenceDict['6'] = 'sixteen hundred '
    hundredsTeensSequenceDict['7'] = 'seventeen hundred '
    hundredsTeensSequenceDict['8'] = 'eighteen hundred '
    hundredsTeensSequenceDict['9'] = 'nineteen hundred '

    thousandsSequenceDict['1'] = 'one thousand '
    thousandsSequenceDict['2'] = 'two thousand '
    thousandsSequenceDict['3'] = 'three thousand '
    thousandsSequenceDict['4'] = 'four thousand '
    thousandsSequenceDict['5'] = 'five thousand '
    thousandsSequenceDict['6'] = 'six thousand '
    thousandsSequenceDict['7'] = 'seven thousand '
    thousandsSequenceDict['8'] = 'eight thousand '
    thousandsSequenceDict['9'] = 'nine thousand '

    generalSymbolsDict['-'] = '<one-of><item repeat="0-1">dash</item><item repeat="0-1">hyphen</item></one-of>'
    generalSymbolsDict['_'] = '<one-of><item repeat="0-1">underscore</item></one-of>'
    generalSymbolsDict['.'] = '<one-of><item>point</item></one-of>'

    generalDecimalNamesDict[1] = 'tenths'
    generalDecimalNamesDict[2] = 'hundredths'
    generalDecimalNamesDict[3] = 'thousandths'
    generalDecimalNamesDict[4] = 'ten thousandths'
    generalDecimalNamesDict[5] = 'hundred thousandths'
    generalDecimalNamesDict[6] = 'millionths'
    generalDecimalNamesDict[7] = 'ten millionths'
    generalDecimalNamesDict[8] = 'hundred millionths'
    generalDecimalNamesDict[9] = 'billionths'
    generalDecimalNamesDict[10] = 'ten billionths'
    generalDecimalNamesDict[11] = 'hundred billionths'
    generalDecimalNamesDict[12] = 'trillionths'

    decimalConnector = ' <item repeat="0-1"> and </item> '

    generalOnesDict['0'] = 'zero'
    generalOnesDict['1'] = 'one'
    generalOnesDict['2'] = 'two'
    generalOnesDict['3'] = 'three'
    generalOnesDict['4'] = 'four'
    generalOnesDict['5'] = 'five'
    generalOnesDict['6'] = 'six'
    generalOnesDict['7'] = 'seven'
    generalOnesDict['8'] = 'eight'
    generalOnesDict['9'] = 'nine'

    generalTensDict['1'] = 'ten'
    generalTensDict['2'] = 'twenty'
    generalTensDict['3'] = 'thirty'
    generalTensDict['4'] = 'forty'
    generalTensDict['5'] = 'fifty'
    generalTensDict['6'] = 'sixty'
    generalTensDict['7'] = 'seventy'
    generalTensDict['8'] = 'eighty'
    generalTensDict['9'] = 'ninety'

    generalTeensDict['1'] = 'eleven'
    generalTeensDict['2'] = 'twelve'
    generalTeensDict['3'] = 'thirteen'
    generalTeensDict['4'] = 'fourteen'
    generalTeensDict['5'] = 'fifteen'
    generalTeensDict['6'] = 'sixteen'
    generalTeensDict['7'] = 'seventeen'
    generalTeensDict['8'] = 'eighteen'
    generalTeensDict['9'] = 'nineteen'

    tripleOnesDict['0'] = 'zero'
    tripleOnesDict['1'] = 'one'
    tripleOnesDict['2'] = 'two'
    tripleOnesDict['3'] = 'three'
    tripleOnesDict['4'] = 'four'
    tripleOnesDict['5'] = 'five'
    tripleOnesDict['6'] = 'six'
    tripleOnesDict['7'] = 'seven'
    tripleOnesDict['8'] = 'eight'
    tripleOnesDict['9'] = 'nine'

    prefabGrammarstoGen['YESNO_SIMPLE'] = '<rule id="YESNO_SIMPLE" scope="public">\n\t<one-of><item>yes <tag>ZVAL=&apos;yes&apos;</tag></item><item>no <tag>ZVAL=&apos;no&apos;</tag></item></one-of>\n</rule>'
    prefabGrammarstoGen['YESNO_EXPANDED'] = '<rule id="YESNO_SIMPLE" scope="public">\n\t<one-of><item>yes <tag>ZVAL=&apos;yes&apos;</tag></item><item>no <tag>ZVAL=&apos;no&apos;</tag></item></one-of>\n</rule>'
    prefabGrammarstoGen['HMWSE'] = '<rule id="HMWSE" scope="public">\n\t<one-of><item>help me with something else</item></one-of><tag>ZVAL=&apos;HMWSE&apos;</tag>\n</rule>'
    prefabGrammarstoGen['UNIVERSALS'] = '<rule id="UNIVERSALS" scope="public">\n\t<one-of><item>universals</item></one-of>\n</rule>'
    prefabGrammarstoGen['THANKS'] = '<rule id="THANKS" scope="public">\n\t<one-of><item>thank you</item><item>thanks</item></one-of>\n</rule>'
    prefabGrammarstoGen['UHUM'] = '<rule id="UHUM" scope="public">\n\t<one-of><item>uh</item><item>um</item></one-of>\n</rule>'
    prefabGrammarstoGen['PLEASE'] = '<rule id="PLEASE" scope="public">\n\t<one-of><item>please</item></one-of>\n</rule>'

  elif 'es-' in language:
    greaterTensConnector = ' y '
    tensOnesConnector = ' y '
	
    triplesNameDict[0] = 'mil'
    triplesNameDict[1] = 'millón'
    triplesNameDict[2] = 'mil millón'
    triplesNameDict[3] = 'billón'
    triplesNameDict[4] = 'mil billón'
    triplesNameDict[5] = 'trillón'
    triplesNameDict[6] = 'mil trillón'
    triplesNameDict[7] = 'quatrillón'
    triplesNameDict[8] = 'mil quatrillón'
  
    triplesNamePluralDict[0] = 'mil'
    triplesNamePluralDict[1] = 'milliones'
    triplesNamePluralDict[2] = 'mil milliones'
    triplesNamePluralDict[3] = 'billiones'
    triplesNamePluralDict[4] = 'mil billiones'
    triplesNamePluralDict[5] = 'trilliones'
    triplesNamePluralDict[6] = 'mil trilliones'
    triplesNamePluralDict[7] = 'quatrilliones'
    triplesNamePluralDict[8] = 'mil quatrilliones'
  
    hundredsSequenceDict['0'] = 'cien '
    hundredsSequenceDict['1'] = 'ciento '
    hundredsSequenceDict['2'] = 'doscientos '
    hundredsSequenceDict['3'] = 'trescientos '
    hundredsSequenceDict['4'] = 'cuatrocientos '
    hundredsSequenceDict['5'] = 'quinientos '
    hundredsSequenceDict['6'] = 'seiscientos '
    hundredsSequenceDict['7'] = 'setecientos '
    hundredsSequenceDict['8'] = 'ochocientos '
    hundredsSequenceDict['9'] = 'novecientos '

    hundredsTeensSequenceDict['1'] = 'once cientos '
    hundredsTeensSequenceDict['2'] = 'doce cientos '
    hundredsTeensSequenceDict['3'] = 'rece cientos '
    hundredsTeensSequenceDict['4'] = 'catorce cientos '
    hundredsTeensSequenceDict['5'] = 'quince cientos '
    hundredsTeensSequenceDict['6'] = 'dieciseis cientos '
    hundredsTeensSequenceDict['7'] = 'diecisiete cientos '
    hundredsTeensSequenceDict['8'] = 'dieciocho cientos '
    hundredsTeensSequenceDict['9'] = 'diecinueve cientos '

    thousandsSequenceDict['1'] = 'mil '
    thousandsSequenceDict['2'] = 'dos mil '
    thousandsSequenceDict['3'] = 'tres mil '
    thousandsSequenceDict['4'] = 'cuatro mil '
    thousandsSequenceDict['5'] = 'cinco mil '
    thousandsSequenceDict['6'] = 'seis mil '
    thousandsSequenceDict['7'] = 'siete mil '
    thousandsSequenceDict['8'] = 'ocho mil '
    thousandsSequenceDict['9'] = 'nueve mil '

    generalSymbolsDict['-'] = ' <one-of><item repeat="0-1">guión</item></one-of> '
    generalSymbolsDict['_'] = ' <one-of><item repeat="0-1">guión bajo</item></one-of> '
    generalSymbolsDict['.'] = '<one-of><item>punto</item></one-of>'

    generalDecimalNamesDict[1] = 'décimas'
    generalDecimalNamesDict[2] = 'centésimas'
    generalDecimalNamesDict[3] = 'milésimas'
    generalDecimalNamesDict[4] = 'diez milésimas'
    generalDecimalNamesDict[5] = 'cien milésimas'
    generalDecimalNamesDict[6] = 'millonésimas'
    generalDecimalNamesDict[7] = 'diez millonésimas'
    generalDecimalNamesDict[8] = 'cien millonésimas'
    generalDecimalNamesDict[9] = 'billonésimas'
    generalDecimalNamesDict[10] = 'diez billonésimas'
    generalDecimalNamesDict[11] = 'cien billonésimas'
    generalDecimalNamesDict[12] = 'trillonésimas'

    decimalConnector = ' <item repeat="0-1"> con </item> '

    generalOnesDict['0'] = 'cero'
    generalOnesDict['1'] = 'uno'
    generalOnesDict['2'] = 'dos'
    generalOnesDict['3'] = 'tres'
    generalOnesDict['4'] = 'cuatro'
    generalOnesDict['5'] = 'cinco'
    generalOnesDict['6'] = 'seis'
    generalOnesDict['7'] = 'siete'
    generalOnesDict['8'] = 'ocho'
    generalOnesDict['9'] = 'nueve'

    generalTensDict['1'] = 'diez'
    generalTensDict['2'] = 'veinte'
    generalTensDict['3'] = 'trenta'
    generalTensDict['4'] = 'cuarenta'
    generalTensDict['5'] = 'cinquenta'
    generalTensDict['6'] = 'sesenta'
    generalTensDict['7'] = 'setenta'
    generalTensDict['8'] = 'ochenta'
    generalTensDict['9'] = 'noventa'

    generalTeensDict['1'] = 'once'
    generalTeensDict['2'] = 'doce'
    generalTeensDict['3'] = 'trece'
    generalTeensDict['4'] = 'catorce'
    generalTeensDict['5'] = 'quince'
    generalTeensDict['6'] = 'dieciséis'
    generalTeensDict['7'] = 'diecisiete'
    generalTeensDict['8'] = 'dieciocho'
    generalTeensDict['9'] = 'diecinueve'

    tripleOnesDict['0'] = 'cero'
    tripleOnesDict['1'] = 'un'
    tripleOnesDict['2'] = 'dos'
    tripleOnesDict['3'] = 'tres'
    tripleOnesDict['4'] = 'cuatro'
    tripleOnesDict['5'] = 'cinco'
    tripleOnesDict['6'] = 'seis'
    tripleOnesDict['7'] = 'siete'
    tripleOnesDict['8'] = 'ocho'
    tripleOnesDict['9'] = 'nueve'

    prefabGrammarstoGen['YESNO_SIMPLE'] = '<rule id="YESNO_SIMPLE" scope="public">\n\t<one-of><item>yes <tag>ZVAL=&apos;si&apos;</tag></item><item>no <tag>ZVAL=&apos;no&apos;</tag></item></one-of>\n</rule>'
    prefabGrammarstoGen['YESNO_EXPANDED'] = '<rule id="YESNO_SIMPLE" scope="public">\n\t<one-of><item>si <tag>ZVAL=&apos;yes&apos;</tag></item><item>no <tag>ZVAL=&apos;no&apos;</tag></item></one-of>\n</rule>'
    prefabGrammarstoGen['HMWSE'] = '<rule id="HMWSE" scope="public">\n\t<one-of><item>ayudame con algol más</item></one-of><tag>ZVAL=&apos;HMWSE&apos;</tag>\n</rule>'
    prefabGrammarstoGen['UNIVERSALS'] = '<rule id="UNIVERSALS" scope="public">\n\t<one-of><item>universals</item></one-of>\n</rule>'
    prefabGrammarstoGen['THANKS'] = '<rule id="THANKS" scope="public">\n\t<one-of><item>gracias</item><item>muchas gracias</item></one-of>\n</rule>'
    prefabGrammarstoGen['UHUM'] = '<rule id="UHUM" scope="public">\n\t<one-of><item>uh</item><item>um</item></one-of>\n</rule>'
    prefabGrammarstoGen['PLEASE'] = '<rule id="PLEASE" scope="public">\n\t<one-of><item>por favor</item></one-of>\n</rule>'


  for elem in truth.split(','):
    elemChange = elem
    if '[' in elemChange or '(' in elemChange:
      prefabCollector = {}
      addGrammars = 1
      buildtruth = buildtruth + newline + replacePattern(elemChange, required_type, dtmf, addGrammarDict_DTMF, addGrammarDict, tripleOnesDict, generalSymbolsDict, generalOnesDict, generalTensDict, generalTeensDict, triplesNameDict, triplesNamePluralDict, hundredsSequenceDict, hundredsTeensSequenceDict, thousandsSequenceDict, triplesLevel, triplesLimitDict, greaterTensConnector, tensOnesConnector, generalDecimalNamesDict, prefabGrammars, prefabCollector, decimalConnector, language)
    else:
      if required_type == 'alphanum':
        elemChange = replaceAlphanum(elemChange, dtmf, language)
        buildtruth = buildtruth + newline + '<item>' + elemChange + '<tag>RETVAL=&apos;' + elem + '&apos;</tag></item>'

    newline = '\n\t\t'

  builddecoy = ''
  if decoy != None:
    builddecoy = '\t<!-- ### Decoy Grammar ### -->\n\t<rule id="decoyITEMS">\n\t\t<one-of>\n\t\t\t'
    newline = ''
    for elem in decoy.split(','):
      elemChange = elem
      if required_type == 'alphanum':
        elemChange = replaceAlphanum(elemChange, dtmf, language)

      builddecoy = builddecoy+newline+"<item>"+elemChange+"</item>"
      newline = '\n\t\t'

    builddecoy = builddecoy+'\n\t\t</one-of>\n\t\t<tag>RETVAL=&apos;Dummy&apos;</tag>\n\t</rule>'

  for elem in range(0, 10):
    dtmfNumRetvalDict[elem] = str(elem)

  for elem in dtmf_return_values_array:
    (dtmfkey, rVal) = elem.split('^')
    if dtmfkey in generalDTMFSymbolsDict.keys():
      dtmfSymbolRetvalDict[generalDTMFSymbolsDict[dtmfkey]] = rVal
    else:
      dtmfNumRetvalDict[int(dtmfkey)] = rVal

  if weight is None:
    weight = default_weight

  mode = default_mode
  if dtmf == 'true':
    mode = 'dtmf'

  addUpperGrammarList = ''
  addMiddleGrammarList = ''
  addLowerGrammarList = ''
  separator = ''
  grammarBuildListUpper = ''
  if addGrammars == 1:
    for elem in addGrammarDict:
      if 'GenSingleDigits' in elem:
        grammarBuildListUpper = createVoiceGrammar(elem, 'VoiceSingleDigits')
        addGrammarDictLower['VoiceSingleDigits'] = 1
      elif 'GenExtendedDigits' in elem:
        grammarBuildListUpper = createVoiceGrammar(elem, 'VoiceExtendedDigits')
        addGrammarDictLower['VoiceSingleDigits'] = 1
        addGrammarDictLower['VoiceExtendedDigits'] = addGrammarDict[elem]
      elif 'GenSingleAlphaNum' in elem:
        grammarBuildListUpper = createVoiceGrammar(elem, 'VoiceSingleAlphaNum')
        addGrammarDictLower['VoiceSingleAlphaNum'] = 1
      elif 'GenExtendedAlphaNum' in elem:
        grammarBuildListUpper = createVoiceGrammar(elem, 'VoiceExtendedAlphaNum')
        addGrammarDictLower['VoiceSingleAlphaNum'] = 1
        addGrammarDictLower['VoiceExtendedAlphaNum'] = addGrammarDict[elem]
      elif 'GenSingleAlphaOnly' in elem:
        grammarBuildListUpper = createVoiceGrammar(elem, 'VoiceSingleAlphaOnly')
        addGrammarDictLower['VoiceSingleAlphaOnly'] = 1
      elif 'GenExtendedAlphaOnly' in elem:
        grammarBuildListUpper = createVoiceGrammar(elem, 'VoiceExtendedAlphaOnly')
        addGrammarDictLower['VoiceSingleAlphaOnly'] = 1
        addGrammarDictLower['VoiceExtendedAlphaOnly'] = addGrammarDict[elem]

      addUpperGrammarList = addUpperGrammarList + separator + grammarBuildListUpper
      separator = '\n\n'

    separator = ''
    for elem in addGrammarDict_DTMF:
      if 'GenSingleDigits_DTMF' in elem:
        grammarBuildListUpper = createDTMFGrammar(elem, 'DTMFSingleDigits')
        addGrammarDictLower['DTMFSingleDigits'] = 1
      elif 'GenSingleAlphaNum_DTMF' in elem:
        grammarBuildListUpper = createDTMFGrammar(elem, 'DTMFSingleAlphaNum')
        addGrammarDictLower['DTMFSingleAlphaNum'] = 1
      elif 'GenSingleAlphaOnly_DTMF' in elem:
        grammarBuildListUpper = createDTMFGrammar(elem, 'DTMFSingleAlphaOnly')
        addGrammarDictLower['DTMFSingleAlphaOnly'] = 1

      addUpperGrammarList = addUpperGrammarList + separator + grammarBuildListUpper
      separator = '\n\n'

    separator = ''
    for grammarName in prefabCollector:
      grammarBuildListMiddle = prefabGrammarstoGen[grammarName]
      addMiddleGrammarList = addMiddleGrammarList + separator + grammarBuildListMiddle
      separator = '\n\n'

    separator = ''
    for elem in addGrammarDictLower:
      if 'VoiceSingleDigits' in elem:
        grammarBuildListLower = createVoiceSingleDigitsGrammar(elem, generalOnesDict, language)
      elif 'VoiceExtendedDigits' in elem:
        grammarBuildListLower = createVoiceExtendedDigitsGrammar(elem, generalOnesDict, addGrammarDictLower[elem], language)
      elif 'VoiceSingleAlphaNum' in elem:
        grammarBuildListLower = createVoiceSingleAlphaNumGrammar(elem, generalOnesDict, language)
#      elif 'VoiceExtendedAlphaNum' in elem:
#        grammarBuildListLower = createVoiceExtendedAlphaNumGrammar(elem, generalOnesDict, addGrammarDictLower[elem], language)
      elif 'VoiceSingleAlphaOnly' in elem:
        grammarBuildListLower = createVoiceSingleAlphaOnlyGrammar(elem, language)
#      elif 'VoiceExtendedAlphaOnly' in elem:
#        grammarBuildListLower = createVoiceExtendedAlphaOnlyGrammar(elem, addGrammarDictLower[elem], language)
      elif 'DTMFSingleDigits' in elem:
        grammarBuildListLower = createDTMFSingleDigitsGrammar(elem, dtmfNumRetvalDict, dtmfSymbolRetvalDict, dtmf_limit, language)
      elif 'DTMFSingleAlphaNum' in elem:
        grammarBuildListLower = createDTMFSingleAlphaNumGrammar(elem, language)
#      elif 'DTMFExtendedAlphaNum' in elem:
#        grammarBuildListLower = createDTMFExtendedAlphaNumGrammar(elem, addGrammarDictLower[elem], language)
      elif 'DTMFSingleAlphaOnly' in elem:
        grammarBuildListLower = createDTMFSingleAlphaOnlyGrammar(elem, language)
#      elif 'DTMFExtendedAlphaOnly' in elem:
#        grammarBuildListLower = createDTMFExtendedAlphaOnlyGrammar(elem, addGrammarDictLower[elem], language)

      addLowerGrammarList = addLowerGrammarList + separator + grammarBuildListLower
      separator = '\n\n'

  rendered_grammar = grammar.format(
    required_type=required_type,
    truth=buildtruth,
    decoy=builddecoy,
    dweight=dweight,
    slot_name=slot_name,
    weight=weight,
    mode=mode,
    language=language,
    decoyTopRule=decoyTopRule,
    addUpperGrammarList=addUpperGrammarList,
    addMiddleGrammarList=addMiddleGrammarList,
    addLowerGrammarList=addLowerGrammarList,
  )

  if errors.messages:
    return errors.render()

  return HttpResponse(rendered_grammar)

gengrammar.info = gengrammar_info
