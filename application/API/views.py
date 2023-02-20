from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from API.permissions import IsAuthor, IsSafeMethod
from API.models import Project, Contributor, Issue, Comment
from API.serializers import ProjectSerializer, ProjectDetailSerializer, ContributorSerializer, UserSerializer, IssueSerializer, CommentSerializer
from authentication.models import User

class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated & (IsAuthor|IsSafeMethod)]

    def get_queryset(self):
        queryset = Project.objects.filter(contributors=self.request.user)
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    @transaction.atomic
    def create(self, request):
        serializer = ProjectDetailSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = ProjectDetailSerializer(instance=instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(status=status.HTTP_200_OK)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_200_OK)

class UsersViewset(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated & (IsAuthor|IsSafeMethod)]

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("project_pk")
        instance = get_object_or_404(Project, id=project_id, contributors=self.request.user)
        users_queryset = User.objects.filter(contributions=instance)
        return users_queryset
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=self.kwargs.get("project_pk"), contributors=self.request.user)
        serializer = ContributorSerializer(data=request.data, context={'project': project})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=self.kwargs.get("project_pk"), contributors=self.request.user)
        user = self.get_object()
        contributor = Contributor.objects.get(project_id=project, user_id=user)
        contributor.delete()
        return Response(status=status.HTTP_200_OK)

class IssuesViewset(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated & IsAuthor]

    def get_queryset(self, *args, **kwargs):
        projects = Project.objects.filter(contributors=self.request.user)
        project = get_object_or_404(projects, id=self.kwargs.get("project_pk"))
        return Issue.objects.filter(project_id=project)
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        projects = Project.objects.filter(contributors=self.request.user)
        project = get_object_or_404(projects, id=self.kwargs.get("project_pk"))
        serializer = IssueSerializer(data=request.data, context={'project': project, 'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = IssueSerializer(instance=instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(status=status.HTTP_200_OK)
    
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_200_OK)

class CommentsViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated & (IsAuthor|IsSafeMethod)]

    def get_queryset(self, *args, **kwargs):
        projects = Project.objects.filter(contributors=self.request.user)
        project = get_object_or_404(projects, id=self.kwargs.get("project_pk"))
        issue = get_object_or_404(Issue, project_id=project, id=self.kwargs.get("issue_pk"))
        return Comment.objects.filter(issue_id=issue)
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        projects = Project.objects.filter(contributors=self.request.user)
        project = get_object_or_404(projects, id=self.kwargs.get("project_pk"))
        issue = get_object_or_404(Issue, project_id=project, id=self.kwargs.get("issue_pk"))
        serializer = CommentSerializer(data=request.data, context={'issue': issue, 'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CommentSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(status=status.HTTP_200_OK)
    
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_200_OK)
