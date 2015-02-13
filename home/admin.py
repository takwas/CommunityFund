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

class UserInterestsAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserInterests, UserInterestsAdmin)

class CommunityInterestsAdmin(admin.ModelAdmin):
    pass
admin.site.register(CommunityInterests, CommunityInterestsAdmin)

class ProjectReputationAdmin(admin.ModelAdmin):
    pass
admin.site.register(ProjectReputation, ProjectReputationAdmin)

class UserReputationAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserReputation, UserReputationAdmin)

class LikeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Like, LikeAdmin)