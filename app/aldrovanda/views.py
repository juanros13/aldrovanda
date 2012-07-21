# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseServerError
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.utils import simplejson
from aldrovanda.models import Product, Image, Category
from mptt.utils import *

# Create your views here.
def index(request):
	#return HttpResponse("Hello, world. Youre at the poll index.")
	latest_products_list = Product.objects.filter(image__default=True).order_by('-creation_date')[:16]
	category_list = Category.objects.filter(parent__isnull=True)[:16]
	if request.user.is_authenticated():
		# Do something for authenticated users.
		user = request.user
	else:
		user = False
    # Do something for anonymous users.
	#t = loader.get_template('products/index.html')
	#c = Context({
	#	'latest_products_list': latest_product_list,
	#})
	#return HttpResponse(t.render(c))
	return render_to_response('aldrovanda/home.html', 
							 	{
									'latest_products_list': latest_products_list,
									'category_list': category_list,
								}, context_instance=RequestContext(request))
def detail(request, product_id):
	#return HttpResponse("Mostrando el producto %s" % product_id)
	p = get_object_or_404(Product, pk=product_id)
	#c = p.category.get_categories_with_links()
	category_list = p.category
	#rating_list = Rating.objects.all().order_by('-value')[:5]
	return render_to_response('aldrovanda/product.html', {
		'product': p,
		'category': category_list,
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
	
	products_list = Product.objects.filter(category__in=category_list_children).order_by('creation_date')
	
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
	if(username):
		#return HttpResponse(username.email)
		return render_to_response('aldrovanda/shop.html', {
			'username': username,
		}, context_instance=RequestContext(request))
	
	