from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('users.views',
    # Examples:
    # url(r'^$', 'app.views.home', name='home'),
    # url(r'^app/', include('app.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^login/$', 'login'),
    url(r'^register/$', 'register'),
    url(r'^logout/$', 'disconnect'),
    url(r'^confirm/$', 'confirm'),
    url(r'^recuperar_clave/$', 'pass_recovery'),
    url(r'^olvide_mi_clave/$', 'forgot_password'),
    url(r'^forgot_password_send_mail/$', 'forgot_password_send_mail'),
    url(r'^save_password/$', 'pass_recovery_save'),
    url(r'^test/$', 'test'),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 