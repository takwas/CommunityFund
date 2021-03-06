from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import *

# Add each model to django admin site so that we can edit them

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


class MemberAdmin(admin.ModelAdmin):
    pass
admin.site.register(Member, MemberAdmin)


class CommentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Comment, CommentAdmin)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserProfileAdmin(UserAdmin):
    inlines=(UserProfileInline,)

# Unregister User because we're extending it to UserProfile
admin.site.unregister(get_user_model())

# Register User extended with UserProfile attributes
admin.site.register(get_user_model(), UserProfileAdmin)
