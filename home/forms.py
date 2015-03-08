import floppyforms.__future__ as forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from .models import *

class ProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit"))

        self.fields['funding_goal'] = forms.DecimalField(min_value=1)

    class Meta:

        model = Project
        exclude = ("initiator", "pub_date", "current_funds", "community")

class MemberForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super(MemberForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit"))

    class Meta:

        model = Member
        exclude = ("user", "community")


class FundForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        print(kwargs)
        max_amount = kwargs.pop('initial', None).pop('max_amount', None)

        super(FundForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit"))

        self.fields['amount'] = forms.IntegerField(min_value=1, max_value=max_amount)

    class Meta:
        model = Funded
        exclude = ("user", "project")


class CommunityForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super(CommunityForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit"))

    class Meta:
        model = Community
        exclude = ("creator",)


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Update"))

    class Meta:
        model = UserProfile
        exclude = ("user",)


class RateUserForm(forms.ModelForm):
    CHOICES=[(1,'1'),
             (2,'2'),
             (3,'3'),
             (4,'4'),
             (5,'5')]

    rating = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):

        super(RateUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Update"))

    class Meta:
        model = UserReputation
        exclude = ("rater", "rated", "project")


class RateProjectForm(forms.ModelForm):
    CHOICES=[(1,'1'),
             (2,'2'),
             (3,'3'),
             (4,'4'),
             (5,'5')]

    rating = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):

        super(RateProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Update"))

    class Meta:
        model = ProjectReputation
        exclude = ("rater", "rated")


class CommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit"))

    class Meta:
        model = Comment
        exclude = ("user", "community", "pub_date")
