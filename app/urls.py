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
    #APP items
    url(r'^items/', include('items.urls')),
    #APP users
    url(r'^user/', include('users.urls')),
    #APP car shopping
    url(r'^tienda/', include('shops.urls')),
    #APP favorite
    url(r'^favorite/', include('favorites.urls')),
    url(r'^vender/$', 'aldrovanda.views.sell'),
    url(r'^usuario/tienda/crear$', 'users.views.user_shop'),
    url(r'^usuario/tienda/validate/$', 'shops.views.shop_validate'),
    url(r'^usuario/tienda/add/$', 'shops.views.shop_add'),
    #APP Categories    
    url(r'^categoryHierarchy/$', 'hierarchy.views.categoryHierarchy'),
    url(r'^categoria/(?P<full_slug>[-\w/]+)/$', 'aldrovanda.views.category'),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

 