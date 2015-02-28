from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from registration.backends.simple.views import RegistrationView
from django.core.urlresolvers import reverse, reverse_lazy
from .models import *
from .forms import *

class HomeView(ListView):

    model = Community

class CustomRegistrationView(RegistrationView):

    def get_success_url(self, request, user):
        return reverse_lazy("home")
    

@login_required
def createProjectView(request, pk):
    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.initiator = request.user
            form_obj.community = Community.objects.get(id=pk)
            form_obj.current_funds = 0
            form_obj.save()

            return HttpResponseRedirect("/")
    else:
        form = ProjectForm()

    return render(request, "project_form.html",
        {'form': form, })


@login_required
def fundProjectView(request, pk):
    if request.method == "POST":
        form = FundForm(request.POST)

        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.user = request.user
            form_obj.project = Project.objects.get(id=pk)
            form_obj.save();

            return HttpResponseRedirect("/")
    else:
        form = FundForm()

    return render(request, "funded_form.html",
        {'form': form, })


class CommunityCreateView(CreateView):
    model = Community
    form_class = CommunityForm

    def form_valid(self, form):
        form_obj = form.save(commit=False)
        form_obj.save();

        return super(CommunityCreateView, self).form_valid(form)

        
class CommunityDetail(DetailView):
    model = Community
    template_name = "community_detail.html"

    def get_context_data(self, **kwargs):
        context = super(CommunityDetail, self).get_context_data(**kwargs)

        print(context)

        comm = context["object"]

        context["projects"] = Project.objects.all().filter(community=comm)

        return context


class ProjectDetail(DetailView):
    model = Project
    template_name = "project_detail.html"

@login_required
def createProject(request, pk):
    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.initiator = request.user
            form_obj.community = Community.objects.get(id=pk)
            form_obj.current_funds = 0
            form_obj.save()

            return HttpResponseRedirect("/")
    else:
        form = ProjectForm()

    return render(request, "project_form.html",
        {'form': form, })



