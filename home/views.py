from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView
from .models import *

class HomeView(ListView):

    model = Project
    
