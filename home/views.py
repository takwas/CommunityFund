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


class HomeView(ListView):

    model = Community


class CommunityListView(ListView):

    model = Community


class CustomRegistrationView(RegistrationView):

    def get_success_url(self, request, user):
        return reverse_lazy("home")


@login_required
def view_profile(request):

    user = request.user
    profile = user.profile
    return render(request, "profile_detail.html", {'user': user, 'profile': profile})


@login_required
def edit_profile(request):

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("profile"))
    else:
        user = request.user
        profile = user.profile

        form = ProfileForm(instance=profile)

    return render(request, "profile_form.html", {'form': form, 'user': user})
    

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
    
    if request.method == "POST":
        form = FundForm(request.POST)

        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.user = request.user

            project = Project.objects.get(id=pk)

            form_obj.project = project
            project.current_funds += form_obj.amount

            project.save()
            form_obj.save()

            return HttpResponseRedirect(reverse('project_details',
                kwargs={'cid': cid, 'pk': pk}))
    else:
        form = FundForm()

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
        context["is_member"] = Member.objects.all().filter(user=self.request.user, community=comm)

        return context


class ProjectDetail(DetailView):
    
    model = Project
    template_name = "project_detail.html"


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
    template_name = "user_detail.html"

    def get_object(self, queryset=None):

        user = super(UserProfileView, self).get_object(queryset)
        UserProfile.objects.get_or_create(user=user)
        return user

class ProjectUpdateView(UpdateView):

    model = Project
    form_class = ProjectForm 

    def get_success_url(self):
        return reverse('project_details', kwargs={'pk': self.kwargs['pk'], 'cid': self.kwargs['cid']})
    

class CommunityUpdateView(UpdateView):

    model = Community
    form_class = CommunityForm

    def get_success_url(self):
        return reverse('community_details', kwargs={'pk': self.kwargs['pk'],})


class ProjectDeleteView(DeleteView):

    model = Project
    success_url = "/"
