from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from registration.backends.simple.views import RegistrationView
from django.core.urlresolvers import reverse, reverse_lazy
from .models import *
from .forms import *

class HomeView(ListView):

    model = Project

class CustomRegistrationView(RegistrationView):

    def get_success_url(self, request, user):
        return reverse_lazy("home")
    
class ProjectCreateView(CreateView):

    model = Project
    form_class = ProjectForm

    def form_valid(self, form):

        form_obj = form.save(commit=False)
        form_obj.initiator = self.request.user
        form_obj.current_funds = 0
        form_obj.save()

        return super(ProjectCreateView, self).form_valid(form)

class FundCreateView(CreateView):

    model = Funded
    form_class = FundForm

    def form_valid(self, form):
        form_obj = form.save(commit=False)
        form_obj.user = self.request.user
        form_obj.save()

        return super(FundCreateView, self).form_valid(form)