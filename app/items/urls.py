from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('items.views',
    # Examples:
    # url(r'^$', 'app.views.home', name='home'),
    # url(r'^app/', include('app.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^(?P<item_id>\d+)/(?P<item_name>[-\w/]+)', 'detail'),
    url(r'^add/image/$', 'upload_image'),
    url(r'^get/tags/$', 'get_tags'),
    url(r'^get/materials/$', 'get_materials'),
    url(r'^crear/product/$', 'user_item'),
    url(r'^add/product/$', 'user_item_add'),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 