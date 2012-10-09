# -*- encoding: utf-8 -*-
import random
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.template import RequestContext
from items.models import Item
from shops.models import Shop, ShopSeccion
from aldrovanda.paginator import Paginator

def shop_detail(request, name, seccion=None):
  shop = get_object_or_404(Shop, name=name)
  user = get_object_or_404(User, username=shop.user.username)
  print user.get_profile()
  # User.objects.get(username=username)
  if seccion:
    items = Item.objects.filter(image__default = True, shop=shop, shopSeccion__name=seccion).order_by('-creation_date')[:16]
  else:
    items = Item.objects.filter(image__default = True, shop=shop).order_by('-creation_date')[:16]

  paginator = Paginator(items, 16) # Show 25 contacts per page
  try:
    page = request.GET.get('page', 1)
  except PageNotAnInteger:
    page = 1


  try:
    items_list = paginator.page(page)
  except PageNotAnInteger:
    # If page is not an integer, deliver first page.
    items_list = paginator.page(1)
  except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
    items_list = paginator.page(paginator.num_pages)

  items_featured_list = Item.objects.filter(image__default = True, shop=shop, featured=True).order_by('-creation_date')[:4]
  
  seccions = ShopSeccion.objects.filter(shop = shop)
  return render_to_response('aldrovanda/shops/detail.html', {
    'user':user,
    'items_list' : items_list,
    'items_featured_list' : items_featured_list,
    'shop' : shop,
    'shop_seccion' : seccions,
    'current_path': request.get_full_path()
  }, context_instance=RequestContext(request))

@require_POST
@login_required
def shop_add(request):
  shopName = request.POST['shop']
  to_return = {'msg' : u'El nombre de la tienda no puede estar en blanco' }
  to_return['success'] = False
  if shopName:
    if not Shop.objects.filter(name=shopName).exists():
      data = {'name' : request.POST['shop'],
              'user' : request.user.id}
      form = ShopForm(data)
      #print form.errors
      if form.is_valid():
        shopNameCleaned = form.cleaned_data['name']
        if not Shop.objects.filter(user=request.user).exists():
          shop = Shop(name=shopNameCleaned, user=request.user)
        else:
          shop = Shop.objects.get(user=request.user)
          shop.name = shopNameCleaned
        shop.save()
        to_return['success'] = True
        to_return['url'] = u'/usuario/item/crear/'
      else:
        to_return['msg'] = form.errors
    else:
      to_return['msg']= {'name' : u'El nombre de la tienda ya esta tomado.'}
  serialized = simplejson.dumps(to_return)
  return HttpResponse(serialized, mimetype="application/json")

@require_POST
@login_required
def shop_validate(request):
  shopName = request.POST['shop']
  to_return = {'success' : False}
  if shopName:
    if not Shop.objects.filter(name=shopName).exists():
      to_return['success'] = True
  serialized = simplejson.dumps(to_return)
  return HttpResponse(serialized, mimetype="application/json")