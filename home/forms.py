import floppyforms.__future__ as forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from .models import *
from decimal import *

class ProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        
        # initiate form, define method, and add Submit button
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit"))

        # validate form field
        self.fields['funding_goal'] = forms.DecimalField(min_value=5, decimal_places=2)

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

        # find maximum amount funder can give to project at current time
        max_amount = kwargs.pop('initial', None).pop('max_amount', None)

        super(FundForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit"))

        min_value = Decimal('0.01')

        self.fields['amount'] = forms.DecimalField(min_value=min_value, 
            max_value=max_amount, decimal_places=2)

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

    cc_number = forms.CharField(label="Credit Card Number", max_length=16, min_length=16, required=False)

    def __init__(self, *args, **kwargs):

        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Update"))

    class Meta:
        model = UserProfile
        exclude = ("user",)


class RateUserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super(RateUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"

    class Meta:
        model = UserReputation
        exclude = ("rater", "rated", "project")


class RateProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super(RateProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"

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
