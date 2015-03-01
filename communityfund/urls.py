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

    url(r'^community/list$', CommunityListView.as_view(), name="comm_list"),

    url(r'^register/$', CustomRegistrationView.as_view(), 
        name="register"),

    url(r'^profile$', view_profile, name="profile"),

    url(r'^profile/edit$', edit_profile, name="edit_profile"),

    url(r'^login/$', "django.contrib.auth.views.login",
        {"template_name": "login.html"}, name="login"),

    url(r'^logout/$', "django.contrib.auth.views.logout",
        {"next_page": "/"}, name="logout"),

    url(r'^community/cid=(?P<pk>\d+)/project/create$', create_project_view, 
        name="project_create"),

    url(r'^community/cid=(?P<cid>\d+)/project/pid=(?P<pk>\d+)/fund$', fund_project_view,
        name="fund_project"),

    url(r'^community/create$', login_required(CommunityCreateView.as_view()),
        name="community_create"),

    url(r'^community/cid=(?P<pk>\d+)/$', login_required(CommunityDetail.as_view()), 
        name="community_details"),

    url(r'^community/cid=(?P<cid>\d+)/project/pid=(?P<pk>\d+)/$', login_required(ProjectDetail.as_view()),
        name="project_details"),

    url(r'^community/cid=(?P<pk>\d+)/join$', join_comm_view, 
        name="join_comm"),
)
