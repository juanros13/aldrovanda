# -*- encoding: utf-8 -*-
import random
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseServerError
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.conf import settings
from django.template import RequestContext
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import permission_required, login_required
from django.utils import simplejson
from shops.models import ShopForm, Shop
from items.models import Item, Image ,Tag, Style, Occasion, Recipient, Material
from users.models import UserDefault
from hierarchy.models import Category
from aldrovanda.paginator import Paginator
from easy_thumbnails.files import get_thumbnailer
from mptt.utils import *




# Create your views here.
def index(request):
	#return HttpResponse("Hello, world. Youre at the poll index.")
	#latest_products_list = Product.objects.filter(image__default=True).order_by('-creation_date')[:8]
	items = Item.objects.filter(image__default=True).order_by('-creation_date')
	paginator = Paginator(items, 12) # Show 25 contacts per page

	
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

	category_list = Category.objects.filter(parent__isnull=True)[:16]

	#if request.user.is_authenticated():
		# Do something for authenticated users.
		#user = request.user
	#else:
		#user = False
    # Do something for anonymous users.
	#t = loader.get_template('products/index.html')
	#c = Context({
	#	'latest_products_list': latest_product_list,
	#})
	#return HttpResponse(t.render(c))

	return render_to_response('aldrovanda/home.html', 
							 	{
									'items_list': items_list,
									'category_list': category_list,
								}, context_instance=RequestContext(request))


def category(request, full_slug):
	#return HttpResponse("Mostrando el producto %s" % product_id)
	category_slugs = full_slug.split('/')
	category = get_object_or_404(Category, slug=category_slugs[-1])
	#validando la url que tiene que ser exacta con los padres desplegada en arbol, de lo contrario
	#de debe enviar un 404 de que no se encontro la categoria
	if category.get_absolute_url() != '/categoria/'+full_slug+'/':
		#raise Http404
		return HttpResponse("No coinciden %s %s" % (category.get_absolute_url(), '/'+full_slug))

	if category.parent :
		if category.get_children() :
			categories_sibling = category.get_siblings(include_self=True)
		else :
			categories_sibling = category.parent.get_siblings(include_self=True)
	else:
		categories_sibling = Category.objects.filter(parent__isnull=True)

	category_list_children = category.get_descendants(include_self=True)

	items = Item.objects.filter(category__in=category_list_children).order_by('creation_date')
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
	#level = category.get
	#
	#test = tree_item_iterator(category)
	#if not '/categoria/'+hierarchy+'/' == category.get_absolute_url():
	#	raise Http404
	#category_slugs = category._recurse_for_parents(category)
    #categories = []
    #category = get_object_or_404(Category, slug=hierarchy)
    #for slug in category_slugs:
    #    if not categories:
    #        parent = None
    #    else:
    #        parent = categories[-1]
    #    category = get_object_or_404(Category, slug=slug, parent=parent)

	
	#rating_list = Rating.objects.all().order_by('-value')[:5]
	return render_to_response('aldrovanda/category.html', {
		'category': category,
		'categories_sibling' : categories_sibling,
		'items_list' : items_list,
		#'parent_category_list' : category._recurse_for_parents(category),
	}, context_instance=RequestContext(request))




def sell(request):

	#if not User.objects.filter(email=email, username=username).exists()
	return render_to_response('aldrovanda/sell.html', {
	}, context_instance=RequestContext(request))







