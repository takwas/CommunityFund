from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from registration.backends.simple.views import RegistrationView
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from .models import *
from .forms import *
from django.db.models import Max, Avg, Sum, Count

# shawty i'm curious eh

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

    def get_success_url(self, request, user):
        return reverse_lazy("home")


@login_required
def create_project_view(request, pk):

    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            comm = get_community(pk)

            form_obj = form.save(commit=False)
            form_obj.initiator = request.user
            form_obj.community = comm
            form_obj.current_funds = 0
            form_obj.save()

            # automatically get added to community if not a member
            obj, created = Member.objects.get_or_create(user=request.user, community=comm)

            return HttpResponseRedirect(reverse('project_details', 
                kwargs={'cid': pk, 'pk': form_obj.id}))
    else:
        form = ProjectForm()

    return render(request, "project_form.html",
        {'form': form, })


@login_required
def join_comm_view(request, pk):

    if request.method == "POST":
        form = MemberForm(request.POST)

        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.user = request.user
            form_obj.community = get_community(pk)
            form_obj.save()

            return HttpResponseRedirect(reverse('community_details', 
                kwargs={'pk': pk,}))
    else:
        form = MemberForm()

    return render(request, "member_form.html",
        {'form': form, })


@login_required
def fund_project_view(request, cid, pk):

    project = get_project(pk)
    
    if request.method == "POST":
        form = FundForm(request.POST)

        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.user = request.user

            form_obj.project = project
            project.current_funds += form_obj.amount

            project.save()
            form_obj.save()

            return HttpResponseRedirect(reverse('project_details',
                kwargs={'cid': cid, 'pk': pk}))
    else:
        max_funds = project.funding_goal - project.current_funds
        form = FundForm(max_amount=max_funds)

    return render(request, "funded_form.html",
        {'form': form, })


class CommunityCreateView(CreateView):
    
    model = Community
    form_class = CommunityForm

    def get_success_url(self):
        return reverse('community_details', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form_obj = form.save(commit=False)
        form_obj.creator = self.request.user
        form_obj.save();

        # automatically get added to community if not a member
        obj, created = Member.objects.get_or_create(user=self.request.user, 
            community_id=form_obj.id)

        return super(CommunityCreateView, self).form_valid(form)

        
class CommunityDetail(DetailView):
    
    model = Community
    template_name = "community_detail.html"

    def get_context_data(self, **kwargs):
        context = super(CommunityDetail, self).get_context_data(**kwargs)
        comm = context["object"]
        context["projects"] = get_all_projects().filter(community=comm)
        context["is_member"] = get_all_members() \
            .filter(user=self.request.user, community=comm)

        return context


class ProjectDetail(DetailView):
    
    model = Project
    template_name = "project_detail.html"

    def get_context_data(self, **kwargs):
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

        print(context["is_member"])

        return context


class MemberListView(ListView):

    model = Member
    template_name = "member_list.html"

    def get_queryset(self):
        return get_all_members().filter(community_id=self.kwargs['pk'])


class UserProfileView(DetailView):

    model = get_user_model()
    slug_field = "username"
    template_name = "profile_detail.html"

    def get_context_data(self, **kwargs):

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

        context["num_projects"] = projects.aggregate(Count('name'))['name__count']

        # get funds given to projects
        context["funds"] = get_all_funds().filter(user=self.request.user)

        # communities
        comms = [x.community for x in get_all_members().filter(user=self.request.user)]
        friends = []

        for item in comms:
            members = get_all_members().filter(community=item) 
            
            for member in members:
                if member.user not in friends and member.user != self.request.user:
                    friends.append(member.user)
        
        context["comms"] = comms
        context["friends"] = friends

        return context


class UserProfileUpdateView(UpdateView):

    model = UserProfile
    form_class = ProfileForm 

    def get_success_url(self):
        return reverse('user_profile', kwargs={'slug': self.request.user.username})


class ProjectUpdateView(UpdateView):

    model = Project
    form_class = ProjectForm 

    def get_success_url(self):
        return reverse('project_details', 
            kwargs={'pk': self.kwargs['pk'], 'cid': self.kwargs['cid']})
    

class CommunityUpdateView(UpdateView):

    model = Community
    form_class = CommunityForm

    def get_success_url(self):
        return reverse('community_details', kwargs={'pk': self.kwargs['pk'],})


class ProjectDeleteView(DeleteView):

    model = Project
    success_url = "/"


@login_required
def rate_initiator_form(request, cid, pk):
    project = get_project(pk)

    if request.method == "POST":
        form = RateUserForm(request.POST)

        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.rater = request.user
            form_obj.rated = project.initiator
            form_obj.project = project

            form_obj.save()

            return HttpResponseRedirect(reverse('project_details',
                kwargs={'cid': cid, 'pk': pk}))
    else:
        form = RateUserForm()

    return render(request, "rate_form.html",
        {'form': form, })


@login_required
def rate_project_form(request, cid, pk):
    project = get_project(pk)

    if request.method == "POST":
        form = RateProjectForm(request.POST)

        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.rater = request.user
            form_obj.rated = project

            form_obj.save()

            return HttpResponseRedirect(reverse('project_details',
                kwargs={'cid': cid, 'pk': pk}))
    else:
        form = RateProjectForm()

    return render(request, "rate_form.html",
        {'form': form, })


@login_required
def funders_list_view(request, cid, pk):
    funders = get_all_funds().filter(project=pk)
    initiator = get_project(pk).initiator

    ratings = UserReputation.objects.all().filter(rater=request.user, project=pk)

    # check who this user has already rated
    rated = []
    for r in ratings:
        rated += [str((get_user(r.rated)))]

    return render(request, "funders_list.html", 
        {'cid': cid, 'pk': pk, 'funders': funders, 'rated': rated, 
         'initiator': initiator})


@login_required
def rate_funder_form(request, cid, pk, funder):
    project = get_project(pk)
    funder = get_user(funder)

    if request.method == "POST":
        form = RateUserForm(request.POST)

        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.rater = request.user
            form_obj.rated = funder
            form_obj.project = project

            form_obj.save()

            return HttpResponseRedirect(reverse('funders_view',
                kwargs={'cid': cid, 'pk': pk}))
    else:
        form = RateUserForm()

    return render(request, "rate_form.html",
        {'form': form, })

def get_project(pid):
    return Project.objects.get(id=pid)

def get_all_projects():
    return Project.objects.all()

def get_community(cid):
    return Community.objects.get(id=cid)

@login_required
def add_comment(request, pk):
    
    comm = get_community(pk)
    
    if request.method == "POST":
        form =  AddCommentForm(request.POST)
        
        if form.is_valid():
            form_obj = form.save(commit = False)
            form_obj.user = request.user
            form_obj.community = comm
            
            form_obj.save()
            
            return HttpResponseRedirect(reverse('community_details', kwargs
                    ={'pk': pk}))
    else:
        form = AddCommentForm()
        
    return render(request, "comment_form.html", {'form': form, })
