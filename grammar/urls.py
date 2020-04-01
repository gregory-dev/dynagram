
from django.urls import path, include

from .methods import methods
from .views import info, methods_info

def generate_paths(method):
  name = method.__name__

  return path(
    '{}/'.format(name),
    include([
      path('info', info(method)),
      path('run', method),
    ]),
  )

methods_urlpatterns = [
  generate_paths(method)
  for method
  in methods
]

info_urlpatterns = [
  path('info', methods_info),
]

urlpatterns = methods_urlpatterns + info_urlpatterns
