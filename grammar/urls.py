
from .methods import methods

from django.http import JsonResponse
from django.urls import path, include

def info(method):
  def view(request):
    return JsonResponse(method.requirements)

  return view

def generate_paths(method):
  name = method.__name__

  return path(
    '{}/'.format(name),
    include([
      path('info', info(method)),
      path('run', method),
    ]),
  )

def methods_info(request):
  info = {
    method.__name__: method.requirements
    for method
    in methods
  }

  return JsonResponse(info)

methods_urlpatterns = [
  generate_paths(method)
  for method
  in methods
]

info_urlpatterns = [
  path('info/', methods_info),
]

urlpatterns = methods_urlpatterns + info_urlpatterns
