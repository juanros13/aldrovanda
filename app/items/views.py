# -*- encoding: utf-8 -*-
import random
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseServerError
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import permission_required, login_required
from django.utils import simplejson
from aldrovanda.paginator import Paginator
from shops.models import ShopForm, Shop
from hierarchy.models import Category
from items.models import Item, Image ,Tag, Style, Occasion, Recipient, Material
from users.models import UserDefault
from favorites.models import Favorite
from easy_thumbnails.files import get_thumbnailer
from mptt.utils import *


def detail(request, item_id, item_name):
  #return HttpResponse("Mostrando el producto %s" % product_id)
  item = get_object_or_404(Item, pk=item_id)
  if item.name != item_name.replace("-", " ").replace ("/", ""):
    return HttpResponseRedirect(item.get_absolute_url())
  #c = p.category.get_categories_with_links()
  category_list = item.category
  item_favorite = False
  if request.user.is_authenticated():
    if Favorite.objects.filter(item=item, user=request.user).exists():
      item_favorite = True

  #rating_list = Rating.objects.all().order_by('-value')[:5]
  return render_to_response('aldrovanda/items/detail.html', {
    'item': item,
    'category': category_list,
    'item_favorite': item_favorite,
  }, context_instance=RequestContext(request))

@login_required
def user_item(request):
  if request.user.is_authenticated():
    if request.user.is_active:
      shop = Shop.objects.filter(user=request.user)
      if shop:
        categories = Category.objects.filter(parent__isnull=True)
        styles = Style.objects.all()
        recipients = Recipient.objects.all()
        occasions = Occasion.objects.all()
        tags = Tag.objects.all()
        return render_to_response('aldrovanda/user_add_product.html', {
          'categories' : categories,
          'styles' : styles,
          'recipients' : recipients,
          'occasions' : occasions,
          'tags' : tags,
        }, context_instance=RequestContext(request))
      else:
        return HttpResponseRedirect(reverse('aldrovanda.views.user_shop'))
    else:
      return HttpResponseRedirect('/')
  else:
    return HttpResponseRedirect(reverse('aldrovanda.views.sell'))

@login_required
def user_item_add(request):

  return render_to_response('aldrovanda/user_add_shop.html', {
  }, context_instance=RequestContext(request))

@require_POST
def upload_image(request):
  print request.FILES
  for upfile in request.FILES.getlist('image-upload'):
    arrayfilename = upfile.name.split('.')
    filename = arrayfilename[0]  + "_" + str(random.randrange(10000,100000)) + "." + arrayfilename[1]
    with open(settings.MEDIA_ROOT + "/uploads/" +filename, 'wb+') as destination:
      for chunk in upfile.chunks():
        destination.write(chunk)
    options = {'size': (280, 160), 'crop': True}
    thumb_url = get_thumbnailer("uploads/" +filename).get_thumbnail(options).url
    print thumb_url
  return HttpResponse(thumb_url)

@require_POST
def get_tags(request):
  query_tag = request.POST['query']
  #test= query_tag, '%'
  tags = Tag.objects.filter(name__icontains=query_tag)
  to_return = []
  if tags:
      for tag in tags:
        to_return.append(tag.name)
  serialized = simplejson.dumps(to_return)
  return HttpResponse(serialized, mimetype="application/json")

@require_POST
def get_materials(request):
  query_tag = request.POST['query']
  #test= query_tag, '%'
  materials = Material.objects.filter(name__icontains=query_tag)
  to_return = []
  if materials:
      for material in materials:
        to_return.append(material.name)
  serialized = simplejson.dumps(to_return)
  return HttpResponse(serialized, mimetype="application/json")
