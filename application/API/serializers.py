from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.db import transaction
from API.models import Project, Contributor
from authentication.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'type', 'author_user_id']
    
    @transaction.atomic
    def create(self, data):
        project = Project.objects.create(**data)
        project.author_user_id = self.context.get('request').user.id
        project.save()
        Contributor.objects.create(
            user_id=self.context.get('request').user,
            project_id=project,
            permission='A',
            role='')
        return project

class ProjectDetailSerializer(ModelSerializer):
    contributors = SerializerMethodField()

    class Meta:
        model = Project
        fields = ['title', 'description', 'type', 'author_user_id', 'contributors']

    def get_contributors(self, instance):
        users_queryset = User.objects.filter(contributions=instance)
        serializer = UserSerializer(users_queryset, many=True)
        return serializer.data

class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['user_id', 'role', 'permission']
    
    @transaction.atomic
    def create(self, data, *args, **kwargs):
        contributor = Contributor.objects.create(
            project_id=self.context.get('project'),
            user_id=data['user_id'],
            permission='C',
            )
        contributor.save()
        return contributor
