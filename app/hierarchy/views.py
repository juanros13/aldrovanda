from django.views.decorators.http import require_POST

# Create your views here.
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