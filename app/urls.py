from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'app.views.home', name='home'),
    # url(r'^app/', include('app.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', 'aldrovanda.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^productos/', include('aldrovanda.urls')),
    url(r'^login/$', 'aldrovanda.views.login'),
    url(r'^register/$', 'aldrovanda.views.register'),
    url(r'^testForm/', 'aldrovanda.views.test'),
    url(r'^logout/$', 'aldrovanda.views.disconnect'),
    url(r'^tienda/(?P<username>\S+)/$', 'aldrovanda.views.shop'),
    url(r'^addFavorite/$', 'aldrovanda.views.addFavorite'),
    url(r'^removeFavorite/$', 'aldrovanda.views.removeFavorite'),
    url(r'^uploadImage/$', 'aldrovanda.views.uploadImage'),
    url(r'^categoryHierarchy/$', 'aldrovanda.views.categoryHierarchy'),
    url(r'^getTags/$', 'aldrovanda.views.getTags'),
    url(r'^getMaterials/$', 'aldrovanda.views.getMaterials'),

    #url(r'^addProduct/', 'aldrovanda.views.disconnect'),
    url(r'^vender/$', 'aldrovanda.views.sell'),
    #url(r'^register/', 'aldrovanda.views.register'),
    #url(r'^categoria/(?P<category_slug>.+?)/?$', 'aldrovanda.views.category'),
    #url(r'^categoria/(?P<category_parent>.+?)/(?P<category_slug>.+?)/?$', 'aldrovanda.views.category_lala')
    url(r'^(?P<full_slug>[-\w/]+)/$', 'aldrovanda.views.category'),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

 