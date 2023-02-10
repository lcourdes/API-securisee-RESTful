from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from API.models import Project, Contributor
from API.serializers import ProjectSerializer, ProjectDetailSerializer, ContributorSerializer, UserSerializer
from authentication.models import User
from rest_framework.exceptions import PermissionDenied

class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Project.objects.filter(contributors=self.request.user)
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    @transaction.atomic
    def create(self, request):
        serializer = ProjectSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.id != instance.author_user_id:
            raise PermissionDenied
        for attribut, value in request.data.items():
            setattr(instance, attribut, value)
        instance.save()
        return Response(status=status.HTTP_200_OK)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.id != instance.author_user_id:
            raise PermissionDenied
        instance.delete()
        return Response(status=status.HTTP_200_OK)

class UsersViewset(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        project_id = self.kwargs.get("project_pk")
        instance = Project.objects.get(id=project_id)
        users_queryset = User.objects.filter(contributions=instance)
        return users_queryset
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        project = Project.objects.get(id=self.kwargs.get("project_pk"))
        serializer = ContributorSerializer(data=request.data, context={'project': project})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        project = Project.objects.get(id=self.kwargs.get("project_pk"))
        if request.user.id != project.author_user_id:
            raise PermissionDenied
        user = User.objects.get(id=self.kwargs.get("pk"))
        contributor = Contributor.objects.get(project_id=project, user_id=user)
        contributor.delete()
        return Response(status=status.HTTP_200_OK)