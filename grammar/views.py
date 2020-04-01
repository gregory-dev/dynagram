
from django.http import JsonResponse

from .methods import methods

def info(method):
  def view(request):
    return JsonResponse(method.info)

  return view

def methods_info(request):
  info = {
    method.__name__: method.info
    for method
    in methods
  }

  return JsonResponse(info)
