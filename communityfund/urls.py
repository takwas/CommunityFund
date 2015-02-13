from django.conf.urls import patterns, include, url
from django.contrib import admin
from home.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'communityfund.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^/', HomeView.as_view(), name="home"),
    url(r'^admin/', include(admin.site.urls)),
)
