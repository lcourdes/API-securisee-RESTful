from django.contrib import admin
from API.models import Project, Contributor, Issue, Comment

admin.site.register(Project)


class ContributorAdmin(admin.ModelAdmin):
    list_display = ["project_id", "user_id"]


admin.site.register(Contributor, ContributorAdmin)


class IssueAdmin(admin.ModelAdmin):
    list_display = ["id", "project_id", "author_user_id"]


admin.site.register(Issue, IssueAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "issue_id", "author_user_id"]


admin.site.register(Comment, CommentAdmin)
