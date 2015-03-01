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

        self.fields['funding_goal'] = forms.IntegerField(min_value=1)

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

        max_amount = kwargs.pop('max_amount', None)

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
