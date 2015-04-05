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


# Views for home page
class HomeView(ListView):
    model = Community


class CommunityListView(ListView):
    model = Community


class CustomRegistrationView(RegistrationView):

    # Return home on succesful registration
    def get_success_url(self, request, user):
        return reverse_lazy("home")
