from .views import *

# Community Related Views
class CommunityCreateView(AjaxCreateView):
    
    model = Community
    form_class = CommunityForm

    def form_valid(self, form):
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
        context["projects"] = get_all_projects().filter(community=comm)

        context["is_member"] = get_all_members() \
            .filter(user=self.request.user, community=comm)

        context["cmnt_list"] = Comment.objects.all().filter(community=comm) \
            .order_by("-pub_date")
        
        context["members"] = get_all_members().filter(community=comm)
        context["profile"] = UserProfile.objects.get(user=self.request.user)

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
        # user and community automatically added, not up to user
        form_obj = form.save(commit=False)
        form_obj.user = self.request.user
        form_obj.community = Community.objects.get(pk=self.kwargs["pk"])
        form_obj.save()

        return super(CommentCreateView, self).form_valid(form)


def search_communities(request):

    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''

    # Simple search using contains
    comm = Community.objects.filter(Q(interests__icontains=search_text) | Q(location__icontains=search_text))

    return render_to_response("community_search.html", {'search_text': search_text,
        'comm': comm})
        