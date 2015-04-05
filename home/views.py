from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from registration.backends.simple.views import RegistrationView
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.db.models import Max, Avg, Sum, Count
from django.db.models import Q
from .models import *
from .forms import *
from fm.views import AjaxCreateView, AjaxUpdateView, AjaxDeleteView


# Helper functions for db queriers
def get_project(pid):
    return Project.objects.get(id=pid)

def get_all_projects():
    return Project.objects.all()

def get_community(cid):
    return Community.objects.get(id=cid)

def get_user(username):
    return User.objects.get(username=username)

def get_all_members():
    return Member.objects.all()

def get_all_funds():
    return Funded.objects.all()


class HomeView(ListView):
    model = Community


class CommunityListView(ListView):
    model = Community


class CustomRegistrationView(RegistrationView):

    # Return home on succesful registration
    def get_success_url(self, request, user):
        return reverse_lazy("home")


# Community Related Views
class CommunityCreateView(AjaxCreateView):
    
    model = Community
    form_class = CommunityForm

    def form_valid(self, form):
        form_obj = form.save(commit=False)

        form_obj.creator = self.request.user

        form_obj.save()

        # automatically get added to community if not a member
        obj, created = Member.objects.get_or_create(user=self.request.user, 
            community_id=form_obj.id)

        return super(CommunityCreateView, self).form_valid(form)


class CommunityDetail(DetailView):
    
    model = Community
    template_name = "community_detail.html"

    def get_context_data(self, **kwargs):

        context = super(CommunityDetail, self).get_context_data(**kwargs)

        # appropriate data used in template
        comm = context["object"]
        context["projects"] = get_all_projects().filter(community=comm)

        context["is_member"] = get_all_members() \
            .filter(user=self.request.user, community=comm)

        context["cmnt_list"] = Comment.objects.all().filter(community=comm) \
            .order_by("-pub_date")
        
        context["members"] = get_all_members().filter(community=comm)
        context["profile"] = UserProfile.objects.get(user__id=self.request.user.id)

        return context


class CommunityUpdateView(AjaxUpdateView):

    model = Community
    form_class = CommunityForm

    def get_queryset(self):
        # filter so that user can't simply type in the update link
        # for stuff they shouldn't be able to edit
        qset = super(CommunityUpdateView, self).get_queryset()
        return qset.filter(creator=self.request.user)


class JoinCommunityView(AjaxCreateView):

    model = Member
    form_class = MemberForm

    def form_valid(self, form):
        
        # the user and community are added by the app
        form_obj = form.save(commit=False)
        form_obj.user = self.request.user
        form_obj.community = get_community(self.kwargs["pk"])

        form_obj.save()

        return super(JoinCommunityView, self).form_valid(form) 


class CommentCreateView(AjaxCreateView):

    model = Comment
    form_class = CommentForm 

    def form_valid(self, form):
        # user and community automatically added, not up to user
        form_obj = form.save(commit=False)
        form_obj.user = self.request.user
        form_obj.community = Community.objects.get(pk=self.kwargs["pk"])
        form_obj.save()

        return super(CommentCreateView, self).form_valid(form)


def search_communities(request):

    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''

    # Simple search using contains
    comm = Community.objects.filter(Q(interests__icontains=search_text) | Q(location__icontains=search_text))

    return render_to_response("community_search.html", {'search_text': search_text,
        'comm': comm})


# Project Related Views
class ProjectCreateView(AjaxCreateView):

    model = Project
    form_class = ProjectForm

    def form_valid(self, form):
        
        # fill in form fields that are not up to user
        comm_id = self.kwargs["pk"]
        comm = get_community(comm_id)

        form_obj = form.save(commit=False)
        form_obj.initiator = self.request.user
        form_obj.community = comm

        ## remove
        form_obj.current_funds = 0

        form_obj.save()

        # automatically get added to community if not a member
        obj, created = Member.objects.get_or_create(user=self.request.user, 
            community=comm)

        return super(ProjectCreateView, self).form_valid(form)


class ProjectDetail(DetailView):
    
    model = Project
    template_name = "project_detail.html"

    def get_context_data(self, **kwargs):

        # appropriate data used in template
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        p = context["object"]
        
        context["did_fund"] = get_all_funds().filter(user=self.request.user, project=p)
        
        context["did_rate_project"] = ProjectReputation.objects.all() \
            .filter(rater=self.request.user, rated=p)
        
        context["did_rate_user"] = UserReputation.objects.all() \
            .filter(rater=self.request.user, rated=p.initiator, project=p)

        ratings = ProjectReputation.objects.all().filter(rated=p)

        context["rating"] = ratings.aggregate(Avg('rating'))['rating__avg']
        context["num_ratings"] = ratings.aggregate(Count('rating'))['rating__count']

        context["is_member"] = get_all_members() \
            .filter(community=p.community, user=self.request.user)

        context["funders"] = get_all_funds().filter(project=p)
        ratings = UserReputation.objects.all().filter(rater=self.request.user, project=p)

        # check who this user has already rated
        rated = []
        for r in ratings:
            rated += [str((get_user(r.rated)))]

        context["rated"] = rated

        context["profile"] = UserProfile.objects.get(user = self.request.user)

        return context


class ProjectUpdateView(AjaxUpdateView):

    model = Project
    form_class = ProjectForm 

    def get_queryset(self):
        # filter so that user can't simply type in the update link
        # for stuff they shouldn't be able to edit
        qset = super(ProjectUpdateView, self).get_queryset()
        return qset.filter(initiator=self.request.user)


class ProjectDeleteView(AjaxDeleteView):

    model = Project
    success_url = "/"

    def get_queryset(self):
        # filter so that user can't simply type in the delete link
        # for stuff they shouldn't be able to edit
        qset = super(ProjectDeleteView, self).get_queryset()
        return qset.filter(initiator=self.request.user)


class FundProjectView(AjaxCreateView):

    model = Funded
    form_class = FundForm

    def get_initial(self):
        # pass in max values for form
        project = get_project(self.kwargs["pk"])
        max_funds = project.funding_goal - project.getCurrentFunds()

        return ({'max_amount': max_funds})

    def form_valid(self, form):

        # fill in fields that user cannot (or should not)
        project = get_project(self.kwargs["pk"])

        form_obj = form.save(commit=False)
        form_obj.user = self.request.user
        form_obj.project = project

        project.save()
        form_obj.save()

        return super(FundProjectView, self).form_valid(form)


class RateProjectView(AjaxCreateView):

    model = ProjectReputation
    form_class = RateProjectForm

    def form_valid(self, form):

        # fill in fields that user cannot
        project = get_project(self.kwargs['pk'])

        form_obj = form.save(commit=False)
        form_obj.rater = self.request.user
        form_obj.rated = project

        form_obj.save()

        return super(RateProjectView, self).form_valid(form)


class RateProjectUpdateView(AjaxUpdateView):

    model = ProjectReputation
    form_class = RateProjectForm

    def get_object(self, queryset=None):
        pid = self.kwargs['pk']
        user_id = self.request.user.id

        rating = ProjectReputation.objects.get(rater=user_id, rated=pid)
        return rating


# User Related Views
class UserProfileView(DetailView):

    model = get_user_model()
    slug_field = "username"
    template_name = "profile_detail.html"

    def get_context_data(self, **kwargs):

        # data used by template (which has access to dict context)
        context = super(UserProfileView, self).get_context_data(**kwargs)
        comm = context["object"]
        user = get_user(self.kwargs["slug"])
        projects = get_all_projects().filter(initiator=user)

        context["projects"] = projects
        context["prof_user"] = user
        context["profile"] = UserProfile.objects.get(user=user)

        ratings = UserReputation.objects.all().filter(rated=user)

        context["rating"] = ratings.aggregate(Avg('rating'))['rating__avg']
        context["num_ratings"] = ratings.aggregate(Count('rating'))['rating__count']

        # get the average of the average ratings for projects
        pratings = []
        for p in projects:
            avg_rating = ProjectReputation.objects.all().filter(rated=p) \
                            .aggregate(Avg('rating'))['rating__avg']
            if avg_rating:
                pratings += [avg_rating]

        if len(pratings) > 0:
            context["prating"] = sum(pratings) / len(pratings)
        else:
            context["prating"] = None

        # get funds given to projects
        context["funds"] = get_all_funds().filter(user=user)

        # communities
        comms = [x.community for x in get_all_members().filter(user=user)]
        friends = []

        # Find all members of all communities the user is in 
        for item in comms:
            members = get_all_members().filter(community=item) 
                
            for member in members:
                if member.user not in friends and member.user != self.request.user:
                    friends.append(member.user)
        
        context["comms"] = comms
        context["friends"] = friends

        return context


class UserProfileUpdateView(AjaxUpdateView):

    model = UserProfile
    form_class = ProfileForm 

    def get_queryset(self):
        # filter so that user can't simply type in the update link
        # for stuff they shouldn't be able to edit
        qset = super(UserProfileUpdateView, self).get_queryset()
        return qset.filter(user=self.request.user)


class RateInitiatorView(AjaxCreateView):

    model = UserReputation
    form_class = RateUserForm

    def form_valid(self, form):

        # fill in stuff user cannot
        project = get_project(self.kwargs['pk'])

        form_obj = form.save(commit=False)
        form_obj.rater = self.request.user
        form_obj.rated = project.initiator
        form_obj.project = project

        form_obj.save()

        return super(RateInitiatorView, self).form_valid(form)


class RateInitiatorUpdateView(AjaxUpdateView):

    model = UserReputation
    form_class = RateUserForm

    def get_object(self, queryset=None):
        pid = self.kwargs['pk']
        user_id = self.request.user.id

        rating = UserReputation.objects.get(rater=user_id, project=pid)
        return rating


class RateFunderView(AjaxCreateView):

    model = UserReputation
    form_class = RateUserForm

    def form_valid(self, form):

        # fill in stuff user cannot
        project = get_project(self.kwargs['pk'])
        funder = get_user(self.kwargs['funder'])

        form_obj = form.save(commit=False)
        form_obj.rater = self.request.user
        form_obj.rated = funder
        form_obj.project = project

        form_obj.save()

        return super(RateFunderView, self).form_valid(form)


class RateFunderUpdateView(AjaxUpdateView):

    model = UserReputation
    form_class = RateUserForm

    def get_object(self, queryset=None):
        pid = self.kwargs['pk']
        user_id = self.request.user.id
        funder = get_user(self.kwargs['funder']).id

        rating = UserReputation.objects.get(rater=user_id, project=pid, rated=funder)
        return rating

