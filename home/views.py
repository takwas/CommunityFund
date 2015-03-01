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
            form_obj = form.save(commit=False)
            form_obj.initiator = request.user
            form_obj.community = Community.objects.get(id=pk)
            form_obj.current_funds = 0
            form_obj.save()

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
            form_obj.community = Community.objects.get(id=pk)
            form_obj.save()

            return HttpResponseRedirect(reverse('community_details', 
                kwargs={'pk': pk,}))
    else:
        form = MemberForm()

    return render(request, "member_form.html",
        {'form': form, })


@login_required
def fund_project_view(request, cid, pk):

    project = Project.objects.get(id=pk)
    
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

        return super(CommunityCreateView, self).form_valid(form)

        
class CommunityDetail(DetailView):
    
    model = Community
    template_name = "community_detail.html"

    def get_context_data(self, **kwargs):
        context = super(CommunityDetail, self).get_context_data(**kwargs)
        comm = context["object"]
        context["projects"] = Project.objects.all().filter(community=comm)
        context["is_member"] = Member.objects.all() \
            .filter(user=self.request.user, community=comm)

        return context


class ProjectDetail(DetailView):
    
    model = Project
    template_name = "project_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        p = context["object"]
        
        context["did_fund"] = Funded.objects.all().filter(user=self.request.user, project=p)
        
        context["did_rate_project"] = ProjectReputation.objects.all() \
            .filter(rater=self.request.user, rated=p)
        
        context["did_rate_user"] = UserReputation.objects.all() \
            .filter(rater=self.request.user, rated=p.initiator, project=p)

        ratings = ProjectReputation.objects.all().filter(rated=p)

        context["rating"] = ratings.aggregate(Avg('rating'))['rating__avg']
        context["num_ratings"] = ratings.aggregate(Count('rating'))['rating__count']

        return context


class MemberListView(ListView):

    model = Member
    template_name = "member_list.html"

    def get_queryset(self):
        
        qset = super(MemberListView, self).get_queryset()
        qset.filter(community=self.kwargs['pk'])
        return qset


class UserProfileView(DetailView):

    model = get_user_model()
    slug_field = "username"
    template_name = "profile_detail.html"

    def get_context_data(self, **kwargs):

        context = super(UserProfileView, self).get_context_data(**kwargs)
        comm = context["object"]
        user = User.objects.get(username=self.kwargs["slug"])
        projects = Project.objects.all().filter(initiator=user)

        context["projects"] = projects
        context["profile"] = user

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


        print(pratings)
        if len(pratings) > 0:
            context["prating"] = sum(pratings) / len(pratings)
        else:
            context["prating"] = None

        context["num_projects"] = projects.aggregate(Count('name'))['name__count']

        print(context["num_projects"])


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
    project = Project.objects.get(id=pk)

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
    project = Project.objects.get(id=pk)

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
    funders = Funded.objects.all().filter(project=pk)

    return render(request, "funders_list.html", 
        {'cid': cid, 'pk': pk, 'funders': funders})


@login_required
def rate_funder_form(request, cid, pk, funder):
    project = Project.objects.get(id=pk)
    funder = User.objects.get(username=funder)

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

