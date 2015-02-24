from django.contrib import admin
from .models import *

class ProjectAdmin(admin.ModelAdmin):
    pass
admin.site.register(Project, ProjectAdmin)

class CommunityAdmin(admin.ModelAdmin):
    pass
admin.site.register(Community, CommunityAdmin)

class FundedAdmin(admin.ModelAdmin):
    pass
admin.site.register(Funded, FundedAdmin)

class ProjectReputationAdmin(admin.ModelAdmin):
    pass
admin.site.register(ProjectReputation, ProjectReputationAdmin)

class UserReputationAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserReputation, UserReputationAdmin)

