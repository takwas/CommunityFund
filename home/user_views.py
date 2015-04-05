from .views import *

# User Related Views
class UserProfileView(DetailView):

    model = get_user_model()
    slug_field = "username"
    template_name = "profile_detail.html"

    def get_context_data(self, **kwargs):

        # data used by template (which has access to dict context)
        context = super(UserProfileView, self).get_context_data(**kwargs)
        comm = context["object"]

        # === ABOUT SECTION ===
        # get the user for the current profile
        user = get_user(self.kwargs["slug"])

        # all ratings given by users to the user this profile belongs to
        ratings = UserReputation.objects.all().filter(rated=user)

        # get the average of all ratings given to the user of this profile
        rating = ratings.aggregate(Avg('rating'))['rating__avg']
        num_ratings = ratings.aggregate(Count('rating'))['rating__count']

        # get the average of the average ratings their projects
        pratings = []
        for p in projects:
            avg_rating = ProjectReputation.objects.all().filter(rated=p) \
                            .aggregate(Avg('rating'))['rating__avg']
            if avg_rating:
                pratings += [avg_rating]

        prating_avg = None
        if len(pratings) > 0:
            prating_avg = sum(pratings) / len(pratings)


        # === PROJECTS SECTION ===
        # get all projects the user this profile belongs to has started
        projects = get_all_projects().filter(initiator=user)


        # === COMMUNITIES SECTION ===
        # get all the communities the user this profile belongs to is a part of
        comms = [x.community for x in get_all_members().filter(user=user)]

        # === FUNDING SECTION ===
        # get funds given to projects by the user this profile belongs to
        funds = get_all_funds().filter(user=user)

        
        # === FRIENDS SECTION ===
        friends = []

        # Find all members of all communities the user is in 
        for item in comms:
            members = get_all_members().filter(community=item) 
                
            for member in members:
                if member.user not in friends and member.user != user:
                    friends.append(member.user)
        

        # Return all the information required to display a user profile
        context["prof_user"] = user
        context["profile"] = UserProfile.objects.get(user=user)
        ontext["rating"] = rating
        context["num_ratings"] = num_ratings
        context["prating"] = prating_avg

        context["projects"] = projects

        context["comms"] = comms
        context["funds"] = funds

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

        # Fill in the fields about who is rating who and for which project
        # The user should only need to provide a number for a rating
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

        # Find the rating object that should be updated
        pid = self.kwargs['pk']
        user_id = self.request.user.id

        rating = UserReputation.objects.get(rater=user_id, project=pid)
        return rating


class RateFunderView(AjaxCreateView):

    model = UserReputation
    form_class = RateUserForm

    def form_valid(self, form):

        # Fill in the fields about who is rating who and for which project
        # The user should only need to provide a number for a rating
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

        # Find the rating object that should be updated
        pid = self.kwargs['pk']
        user_id = self.request.user.id
        funder = get_user(self.kwargs['funder']).id

        rating = UserReputation.objects.get(rater=user_id, project=pid, rated=funder)
        return rating
