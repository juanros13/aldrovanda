from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from aldrovanda.models import Product, Image, Category

# Create your views here.
def index(request):
	#return HttpResponse("Hello, world. Youre at the poll index.")
	latest_products_list = Product.objects.filter(image__default=True).order_by('-creation_date')[:16]
	category_list = Category.objects.filter(parent__isnull=True)[:16]
	#t = loader.get_template('products/index.html')
	#c = Context({
	#	'latest_products_list': latest_product_list,
	#})
	#return HttpResponse(t.render(c))
	return render_to_response('products/home.html', 
							 	{
									'latest_products_list': latest_products_list,
									'category_list': category_list
								})
def detail(request, product_id):
	#return HttpResponse("Mostrando el producto %s" % product_id)
	p = get_object_or_404(Product, pk=product_id)
	#c = p.category.get_categories_with_links()
	category_list = p.category
	#rating_list = Rating.objects.all().order_by('-value')[:5]
	return render_to_response('products/product.html', {
		'product': p,
		'category_list': category_list,
	}, context_instance=RequestContext(request))

def category(request, hierarchy):
	#return HttpResponse("Mostrando el producto %s" % product_id)
	category_slugs = hierarchy.split('/')
	category = get_object_or_404(Category, slug=category_slugs[-1])
	if not '/categoria/'+hierarchy+'/' == category.get_absolute_url():
		raise Http404
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
	return render_to_response('categories/category.html', {
		'category': category.get_absolute_url(),
		'current_category': category,
		#'parent_category_list' : category._recurse_for_parents(category),
	}, context_instance=RequestContext(request))

