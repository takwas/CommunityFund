from .views import *

# Community Related Views
class CommunityCreateView(AjaxCreateView):
    
    model = Community
    form_class = CommunityForm

    def form_valid(self, form):

        # Ensure the creator for this new community is the user who sent
        # the request
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

        # get all projects posted in this community
        projects = get_all_projects().filter(community=comm)

        # get all comments made in the message board for this community
        cmnt_list = Comment.objects.all().filter(community=comm) \
            .order_by("-pub_date")

        # get all members of this community
        members = get_all_members().filter(community=comm)

        # determine permissions this user has for this community depending on
        # whether this user is a member of this community
        is_member = get_all_members() \
            .filter(user=self.request.user, community=comm)

        # get the profile of the current user - used to check for credit card
        # number existence
        profile = UserProfile.objects.get(user=self.request.user)

        # Return all the information required to display a community page
        context["projects"] = projects
        context["cmnt_list"] = cmnt_list
        context["members"] = members
        context["is_member"] = is_member
        context["profile"] = profile

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

        # user and community being posted to automatically added, not up to user
        form_obj = form.save(commit=False)
        form_obj.user = self.request.user
        form_obj.community = Community.objects.get(pk=self.kwargs["pk"])
        form_obj.save()

        return super(CommentCreateView, self).form_valid(form)



# Handle AJAX request when searching for communities
def search_communities(request):

    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''

    # Simple search using contains
    comm = Community.objects.filter(Q(interests__icontains=search_text) | Q(location__icontains=search_text))

    return render_to_response("community_search.html", {'search_text': search_text,
        'comm': comm})
