# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseServerError
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.conf import settings
from django.template import RequestContext
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.utils import simplejson
from aldrovanda.models import Product, Image, Category, UserDefault, Favorite
from aldrovanda.paginator import Paginator
from easy_thumbnails.files import get_thumbnailer
from mptt.utils import *
import random



# Create your views here.
def index(request):
	#return HttpResponse("Hello, world. Youre at the poll index.")
	#latest_products_list = Product.objects.filter(image__default=True).order_by('-creation_date')[:8]
	products = Product.objects.filter(image__default=True).order_by('-creation_date')
	paginator = Paginator(products, 12) # Show 25 contacts per page

	
	try:
		page = request.GET.get('page', 1)
	except PageNotAnInteger:
		page = 1


	try:
		products_list = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		products_list = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		products_list = paginator.page(paginator.num_pages)

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
									'products_list': products_list,
									'category_list': category_list,
								}, context_instance=RequestContext(request))
def detail(request, product_id):
	#return HttpResponse("Mostrando el producto %s" % product_id)
	p = get_object_or_404(Product, pk=product_id)
	#c = p.category.get_categories_with_links()
	category_list = p.category
	product_favorite = False
	if request.user.is_authenticated():
		if Favorite.objects.filter(product=p, user=request.user).exists():
			product_favorite = True

	#rating_list = Rating.objects.all().order_by('-value')[:5]
	return render_to_response('aldrovanda/product.html', {
		'product': p,
		'category': category_list,
		'product_favorite': product_favorite,
	}, context_instance=RequestContext(request))

def category(request, full_slug):
	#return HttpResponse("Mostrando el producto %s" % product_id)
	category_slugs = full_slug.split('/')
	category = get_object_or_404(Category, slug=category_slugs[-1])
	#validando la url que tiene que ser exacta con los padres desplegada en arbol, de lo contrario
	#de debe enviar un 404 de que no se encontro la categoria
	if category.get_absolute_url() != '/'+full_slug+'/':
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

	products = Product.objects.filter(category__in=category_list_children).order_by('creation_date')
	paginator = Paginator(products, 16) # Show 25 contacts per page
	try:
		page = request.GET.get('page', 1)
	except PageNotAnInteger:
		page = 1


	try:
		products_list = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		products_list = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		products_list = paginator.page(paginator.num_pages)
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
		'products_list' : products_list,
		#'parent_category_list' : category._recurse_for_parents(category),
	}, context_instance=RequestContext(request))

@require_POST
def login(request):
	to_return = {'msg':u'Sin datos del POST' }
	to_return['success'] = False
	if request.method == "POST":
		post = request.POST.copy()
		if post.has_key('username') and post.has_key('password'):
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					auth_login(request, user)
					# Redirect to a success page.
					success = True
					to_return['success'] = True
				else :
					# Return a 'disabled account' error message
					to_return['msg'] = u"Tu cuenta ha sido desactivada"
			else :
				# Return an 'invalid login' error message.
				to_return['msg'] = u"Usuario o contraseña invalida"
		else :
			to_return['msg'] = u"No has ingresado usuario ni contraseña."
	serialized = simplejson.dumps(to_return)
	return HttpResponse(serialized, mimetype="application/json")

	

@require_POST
def register(request):
	username = request.POST['username']
	email = request.POST['email']
	password = request.POST['password']
	password_repeat = request.POST['password_repeat']
	first_name = request.POST['first_name']
	last_name = request.POST['last_name']
	if username and email and password and password_repeat and first_name and last_name :
		if password == password_repeat :
			if not User.objects.filter(email=email, username=username).exists():	
				user = User.objects.create_user(username, email, password)
				user.first_name = first_name
				user.last_name = last_name
				user.save()
				return HttpResponse('OK')
			return HttpResponse('ERROR: El ususario y correo ya estan dado de alta')
		return HttpResponse('ERROR: Los password no coinciden ')	
	return HttpResponse('ERROR: Debes llenar todos los campos obligatorios')

@require_POST
def test(request):
	username = request.POST['url']
	if request.is_ajax():
		message = username
		user = authenticate(username='lobo022000', password='activo')

	else:
		message = "Hello"
	return HttpResponse(request)

def disconnect(request):
	logout(request)
	return HttpResponseRedirect('/')

def shop(request, username):
	username = get_object_or_404(User, username=username)# User.objects.get(username=username)
	products = Product.objects.filter(image__default = True, user__username=username).order_by('-creation_date')[:16]

	paginator = Paginator(products, 16) # Show 25 contacts per page
	try:
		page = request.GET.get('page', 1)
	except PageNotAnInteger:
		page = 1


	try:
		products_list = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		products_list = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		products_list = paginator.page(paginator.num_pages)

	if(username):
		#return HttpResponse(username.email)
		return render_to_response('aldrovanda/shop.html', {
			'username' : username,
			'products_list' : products_list,
		}, context_instance=RequestContext(request))

@require_POST
def addFavorite(request):
	to_return = {'msg' : u'Sin datos del POST' }
	to_return['success'] = False
	product_id = request.POST['product_id']
	if request.method == "POST":
		post = request.POST.copy()
		if post.has_key('product_id'):
			if request.user.is_authenticated():
				# Do something for authenticated users.
				user = request.user
				product = get_object_or_404(Product, pk = product_id)
				product_favorite = Favorite(product = product, user = user)
				product_favorite.save()
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
def removeFavorite(request):
	to_return = {'msg' : u'Sin datos del POST' }
	to_return['success'] = False
	product_id = request.POST['product_id']
	if request.method == "POST":
		post = request.POST.copy()
		if post.has_key('product_id'):
			if request.user.is_authenticated():
				# Do something for authenticated users.
				user = request.user
				product = get_object_or_404(Product, pk = product_id)
				product_to_deleted = get_object_or_404(Favorite, product = product, user = user)
				product_to_deleted.delete()
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

def sell(request):
	categories = Category.objects.filter(parent__isnull=True)
	return render_to_response('aldrovanda/sell.html', {
		'categories' : categories
	}, context_instance=RequestContext(request))
	
@require_POST
def uploadImage(request):
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
def categoryHierarchy(request):
	to_return = {'msg' : u'Sin datos del POST' }
	to_return['success'] = False
	category = get_object_or_404(Category, slug=request.POST['category'])
	if category:
		to_return['level'] = category.level
		categories = Category.objects.filter(parent__slug=request.POST['category'])
		to_return['success'] = True
		#category.get_children
		if categories:
			to_return['categories']={}
			for cat in categories:
				to_return['categories'].update({cat.slug: cat.name})
	#listCategory = list(categories)
	#jsonCategory = serializers.serialize('json', listCategory)
	#print request.POST['category']
	#print categories
	#to_return['categories'] = data
	serialized = simplejson.dumps(to_return)
	return HttpResponse(serialized, mimetype="application/json")
