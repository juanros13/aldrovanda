from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('shops.views',
    # Examples:
    # url(r'^$', 'app.views.home', name='home'),
    # url(r'^app/', include('app.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^(?P<name>\S+)/$', 'shop_detail'),
    url(r'^(?P<name>\S+)/seccion/(?P<seccion>\S+)$', 'shop_detail'),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 