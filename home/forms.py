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

    class Meta:

        model = Project
        exclude = ("initiator", "pub_date", "current_funds", "community")

class FundForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(FundForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit"))

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
        exclude = ()
