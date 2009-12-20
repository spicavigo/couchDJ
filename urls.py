from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^couchDJ/', include('couchDJ.foo.urls')),
    (r'^blog/$', 'blog.views.home'),
    (r'^blog/(\d*)/$', 'blog.views.home'),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
)

if settings.LOCAL_DEVELOPMENT:
        urlpatterns += patterns("django.views",
                                url(r"%s(?P<path>.*)/$" %  settings.MEDIA_URL[1:],
                                    "static.serve", {
                                      "document_root": settings.MEDIA_ROOT,
                                  }
                                )
                               )

