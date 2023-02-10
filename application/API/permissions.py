from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.shortcuts import get_object_or_404
from API.models import Project

class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.basename == 'users':
            project = get_object_or_404(Project, id=view.kwargs.get("project_pk"), contributors=request.user)
            if request.user == project.author_user_id:
                return True
        else:
            if obj.author_user_id==request.user:
                return True

class IsSafeMethod(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True