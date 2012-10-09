from django.views.decorators.http import require_POST
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseServerError
from django.utils import simplejson
from items.models import Item
from favorites.models import Favorite

@require_POST
def add_favorite(request):
  to_return = {'msg' : u'Sin datos del POST' }
  to_return['success'] = False
  item_id = request.POST['item_id']
  if request.method == "POST":
    post = request.POST.copy()
    if post.has_key('item_id'):
      if request.user.is_authenticated():
        # Do something for authenticated users.
        user = request.user
        print item_id
        item = get_object_or_404(Item, pk = item_id)
        item_favorite = Favorite(item = item, user = user)
        item_favorite.save()
        to_return['success'] = True
      else:
        #product_favorite = 'Usuario no Logueado redireccionar a la forma login'
        to_return['msg'] = u"Usuario no logueado."
        #return HttpResponseRedirect('/')
    else :
      to_return['msg'] = u"No se proporciono el id para agregar a favoritos."
  else :
    to_return['msg'] = u"No es un POST."
  #return HttpResponseRedirect()
  #return HttpResponse(product_favorite)
  serialized = simplejson.dumps(to_return)
  return HttpResponse(serialized, mimetype="application/json")

@require_POST
def remove_favorite(request):
  to_return = {'msg' : u'Sin datos del POST' }
  to_return['success'] = False
  item_id = request.POST['item_id']
  if request.method == "POST":
    post = request.POST.copy()
    if post.has_key('item_id'):
      if request.user.is_authenticated():
        # Do something for authenticated users.
        user = request.user
        print item_id
        item = get_object_or_404(Item, pk = item_id)
        print item_id
        item_to_deleted = get_object_or_404(Favorite, item = item, user = user)
        print item_id
        item_to_deleted.delete()
        to_return['success'] = True
      else:
        #product_favorite = 'Usuario no Logueado redireccionar a la forma login'
        to_return['msg'] = u"Usuario no logueado."
        #return HttpResponseRedirect('/')
    else :
      to_return['msg'] = u"No se proporciono el id para agregar a favoritos."
  else :
    to_return['msg'] = u"No es un POST."
  #return HttpResponseRedirect()
  #return HttpResponse(product_favorite)
  serialized = simplejson.dumps(to_return)
  return HttpResponse(serialized, mimetype="application/json")# Create your views here.
