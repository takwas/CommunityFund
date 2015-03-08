from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.conf.urls.static import static

from home.views import *

user_urls = patterns('',
    url(r'^register/$', CustomRegistrationView.as_view(), 
        name="register"),

    url(r'^login/$', "django.contrib.auth.views.login",
        {"template_name": "login.html"}, name="login"),

    url(r'^logout/$', "django.contrib.auth.views.logout",
        {"next_page": "/"}, name="logout"),

    url(r'^user/(?P<slug>\w+)/$', UserProfileView.as_view(), name="user_profile"),

    url(r'^user/(?P<pk>\w+)/edit$', login_required(UserProfileUpdateView.as_view()), 
        name="user_profile_edit"),

    url(r'^community/cid=(?P<cid>\d+)/project/pid=(?P<pk>\d+)/rate-initiator$', 
            login_required(RateInitiatorView.as_view()), name="rate_init"),

    url(r'^community/cid=(?P<cid>\d+)/project/pid=(?P<pk>\d+)/funders/rate=(?P<funder>\w+)$', 
            login_required(RateFunderView.as_view()), name="rate_funder")

)

community_urls = patterns('',
    url(r'^search/$', search_communities, name="search_comm"),

    url(r'^community/list$', csrf_exempt(CommunityListView.as_view()), 
        name="comm_list"),

    url(r'^community/create$', login_required(CommunityCreateView.as_view()),
        name="community_create"),

    url(r'^community/cid=(?P<pk>\d+)/$', login_required(CommunityDetail.as_view()), 
        name="community_details"),

    url(r'^community/cid=(?P<pk>\d+)/join$', csrf_exempt(login_required(JoinCommunityView.as_view())), 
        name="join_comm"),

    url(r'^community/cid=(?P<pk>\d+)/comment$', login_required(CommentCreateView.as_view()), 
        name="cmnt_create"),

    url(r'^community/cid=(?P<pk>\d+)/comment/(?P<cmnt_pk>\d+)/delete$', 
        login_required(CommentDeleteView.as_view()), name="cmnt_delete"),

    url(r'^community/cid=(?P<pk>\d+)/comment/(?P<cmnt_pk>\d+)/update$', 
        login_required(CommentUpdateView.as_view()), name="cmnt_update"),

    url(r'^community/cid=(?P<pk>\d+)/members$', MemberListView.as_view(), 
        name="member_list"),

    url(r'^community/cid=(?P<pk>\d+)/update$', login_required(CommunityUpdateView.as_view()), 
        name="comm_update")
)

project_urls = patterns('', 
    url(r'^community/cid=(?P<pk>\d+)/project/create$', login_required(ProjectCreateView.as_view()),
        name="project_create"),

    url(r'^community/cid=(?P<cid>\d+)/project/pid=(?P<pk>\d+)/fund$', 
        login_required(FundProjectView.as_view()), name="fund_project"),

    url(r'^community/cid=(?P<cid>\d+)/project/pid=(?P<pk>\d+)/$', 
        login_required(ProjectDetail.as_view()), name="project_details"),

    url(r'^community/cid=(?P<cid>\d+)/project/pid=(?P<pk>\d+)/update$', 
        login_required(ProjectUpdateView.as_view()), name="project_update"),

    url(r'^community/cid=(?P<cid>\d+)/project/pid=(?P<pk>\d+)/delete$', 
            login_required(ProjectDeleteView.as_view()), name="project_delete"),

    url(r'^community/cid=(?P<cid>\d+)/project/pid=(?P<pk>\d+)/rate-project$', 
            login_required(RateProjectView.as_view()), name="rate_project"),

    url(r'^community/cid=(?P<cid>\d+)/project/pid=(?P<pk>\d+)/funders$', 
            funders_list_view, name="funders_view")
)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', HomeView.as_view(), name="home"),

) + user_urls + community_urls + project_urls

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
