
# Before starting

1. Install Python 3.7
2. Create parent folder for project: `root/`
3. Clone the repository into `root/dynagram`
4. In `root/dynagram`, Setup `python` venv:

`~/root/dynagram/$ path/to/python3.7 -m venv .`

5. Use `pip` to install requirements:

`~/root/dynagram/$ pip install -r requirements.txt`

6. Run tests:

`~/root/dynagram/$ python manage.py test`

You should see an output similar to:

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 0.003s

OK
Destroying test database for alias 'default'...
```

You should now be ready to start development

# Running the server

1. Download ARC (Advanced REST Client), or your REST client of choice
2. Run `runserver`:

`~/root/dynagram/$ python manage.py runserver`

Ensure that the port is `8000` or run with `localhost:8000`:

`~/root/dynagram/$ python manage.py runserver localhost:8000`

3. In the REST client, navigate to `http://localhost:8000/api/info` to see info about installed methods
4. In the REST client, navigate to `http://localhost:8000/api/<method>/info` to info about a specific method, `<method>`.
5. In the REST client, navigate to `http://localhost:8000/api/<method>/run` to run method, `<method>`.

Arguments are accepted in the form `.../run?argument=value&...`

# Adding a new method, `new_grammar`

1. Create a new file called `new_grammar.py`, In the `dynagram/grammar/methods` directory
2. Create a method called `new_grammar`:

```python
# dynagram/grammar/new_grammar.py

from django.http import HttpResponse

def new_grammar(request):
  pass

```

This method currently returns nothing and cannot be used.

3. Add method info. This must be a dictionary containing at least the key `requirements`. The `requirements` value must be a dictionary containing validation information about input parameters.

```python
# dynagram/grammar/new_grammar.py

from django.http import HttpResponse

new_grammar_info = {
  'description': 'The new grammar method',
  'requirements': {
    'name': {
      'type': 'str'
    }
  }
}

def new_grammar(request):
  pass

```

3. Add method validator and pass the `request` and the `info` dictionary:

```python
# dynagram/grammar/methods/new_grammar.py

from django.http import HttpResponse

from .utilities import method_validator

new_grammar_info = {
  'description': 'The new grammar method',
  'requirements': {
    'name': {
      'type': 'str'
    }
  }
}

def new_grammar(request):
  validator, errors = method_validator(info=new_grammar_info, request=request)

```

4. Add the grammar template (some means of rendering the grammar given the input parameters):

```python
# dynagram/grammar/methods/new_grammar.py

from django.http import HttpResponse

from .utilities import method_validator

grammar = '''
<?xml version="1.0" encoding="ISO-8859-1" ?>
<grammar>
  ... {name} ...
</grammar>
'''

new_grammar_info = {
  'description': 'The new grammar method',
  'requirements': {
    'name': {
      'type': 'str'
    }
  }
}

def new_grammar(request):
  validator, errors = method_validator(info=new_grammar_info, request=request)

```

5. Add validation for the desired input parameter (`name`):

```python
# dynagram/grammar/methods/new_grammar.py

from django.http import HttpResponse

from .utilities import method_validator

grammar = '''
<?xml version="1.0" encoding="ISO-8859-1" ?>
<grammar>
  ... {name} ...
</grammar>
'''

new_grammar_info = {
  'description': 'The new grammar method',
  'requirements': {
    'name': {
      'type': 'str'
    }
  }
}

def new_grammar(request):
  validator, errors = method_validator(info=new_grammar_info, request=request)

  name = validator('name')

  rendered_grammar = grammar.format(name=name)

  if errors.messages:
    return errors.render()

  return HttpResponse(rendered_grammar)

```

Also add the final error handler and `HttpResponse` return value:

```python
if errors.messages:
  return errors.render()

return HttpResponse(rendered_grammar)
```

The method can now be run as a request handler.

6. Test the handler's behaviour by writing a test in the `dynagram/grammar/methods/tests` directory.

Name the test `test_<method_name>.py`.
