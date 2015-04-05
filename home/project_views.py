from .views import *

# Project Related Views
class ProjectCreateView(AjaxCreateView):

    model = Project
    form_class = ProjectForm

    def form_valid(self, form):
        
        # Ensure the user who is making this request is the initiator for 
        # the new project and that it will be posted in the community they
        # sent this request from
        comm_id = self.kwargs["pk"]
        comm = get_community(comm_id)

        form_obj = form.save(commit=False)
        form_obj.initiator = self.request.user
        form_obj.community = comm

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

        # the current project
        p = context["object"]
        
        # get all ratings given to this project
        ratings = ProjectReputation.objects.all().filter(rated=p)

        # calculate the average rating given to this project
        rating = ratings.aggregate(Avg('rating'))['rating__avg']
        num_ratings = ratings.aggregate(Count('rating'))['rating__count']

        # determine the permissions this user has

        # determine if the user is a member of the community
        # they will be able to give funds
        is_member = get_all_members() \
            .filter(community=p.community, user=self.request.user)

        # determine if this user has already funded this project
        # they will be allowed to give ratings
        did_fund = get_all_funds().filter(user=self.request.user, project=p)

        # determine if this user has already rated the project and initiator
        # they will be able to update their ratings
        did_rate_project = ProjectReputation.objects.all() \
            .filter(rater=self.request.user, rated=p)

        did_rate_user = UserReputation.objects.all() \
            .filter(rater=self.request.user, rated=p.initiator, project=p)

        # get list of funders
        funders = get_all_funds().filter(project=p)

        # get the profile of the current user - used to check for credit card
        # number existence
        profile = UserProfile.objects.get(user = self.request.user)

        # retrieve the rating given to funders to be used by the project
        # initiator
        fratings = UserReputation.objects.all().filter(rater=self.request.user, project=p)
        rated = []
        for r in fratings:
            rated += [str((get_user(r.rated)))]

        # Return the information needed to display a project 

        context["rating"] = rating
        context["num_ratings"] = num_ratings
        
        context["is_member"] = is_member
        context["did_fund"] = did_fund
        context["did_rate_project"] = did_rate_project
        context["did_rate_user"] = did_rate_user
        
        context["funders"] = funders

        context["rated"] = rated

        context["profile"] = profile

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

        # Fill in the fields about which project is being rated and by who
        # The user should only need to provide a number for a rating
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

        # Find the rating object that should be updated
        pid = self.kwargs['pk']
        user_id = self.request.user.id

        rating = ProjectReputation.objects.get(rater=user_id, rated=pid)
        return rating
