from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from home.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'communityfund.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^register/$', CustomRegistrationView.as_view(), 
        name="register"),

    url(r'^login/$', "django.contrib.auth.views.login",
        {"template_name": "login.html"}, name="login"),

    url(r'^logout/$', "django.contrib.auth.views.logout",
        {"next_page": "/"}, name="logout"),

    url(r'^project/create$', login_required(ProjectCreateView.as_view(success_url="/")),
        name="project_create"),

    url(r'^project/fund$', login_required(FundCreateView.as_view(success_url="/")),
        name="fund_project"),

    url(r'^community/create$', login_required(CommunityCreateView.as_view(success_url="/")),
        name="community_create"),

)
