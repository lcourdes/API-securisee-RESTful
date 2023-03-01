from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError
from django.db import transaction
from API.models import Project, Contributor, Issue, Comment
from authentication.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class UserShortSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'type', 'author_user_id']
    
class ProjectDetailSerializer(ModelSerializer):
    contributors = SerializerMethodField()

    class Meta:
        model = Project
        fields = ['title', 'description', 'type', 'author_user_id', 'contributors']
    
    @transaction.atomic
    def create(self, data):
        project = Project.objects.create(**data)
        project.author_user_id = self.context.get('request').user
        project.save()
        Contributor.objects.create(
            user_id=self.context.get('request').user,
            project_id=project,
            permission='A',
            role='')
        return project

    def get_contributors(self, instance):
        users_queryset = User.objects.filter(contributions=instance)
        serializer = UserShortSerializer(users_queryset, many=True)
        return serializer.data
    
    @transaction.atomic
    def update(self, instance, validated_data):
        if validated_data.get('title'):
            instance.title = validated_data.get('title')
        if validated_data.get('description'):
            instance.description = validated_data.get('description')
        if validated_data.get('type'):
            instance.type = validated_data.get('type')
        instance.save()
        return instance

class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['user_id', 'role', 'permission']
    
    @transaction.atomic
    def create(self, data, *args, **kwargs):
        project = self.context.get('project')
        user = data['user_id']
        if Contributor.objects.filter(project_id=project, user_id=user).exists():
            raise ValidationError('This user is already contributing to project.')
        contributor = Contributor.objects.create(
            project_id=project,
            user_id=user,
            permission='C',
            )
        contributor.save()
        return contributor

class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'created_time', 'title', 'description', 'tag', 'priority', 'status', 'author_user_id', 'assignee_user_id']

    @transaction.atomic
    def create(self, data, *args, **kwargs):
        author = self.context.get('request').user
        project = self.context.get('project')
        if 'assignee_user_id' in data:
            if not Contributor.objects.filter(project_id=project, user_id=data['assignee_user_id']).exists():
                raise ValidationError('The assignee must be a contributor to project.')          
            
        issue = Issue.objects.create(**data, author_user_id=author, project_id=project,)
        if not 'assignee_user_id' in data:
            setattr(issue, 'assignee_user_id', author)
        issue.save()
        return issue
    
    @transaction.atomic
    def update(self, instance, validated_data):
        if validated_data.get('title'):
            instance.title = validated_data.get('title')
        if validated_data.get('description'):
            instance.description = validated_data.get('description')
        if validated_data.get('tag'):
            instance.tag = validated_data.get('tag')
        if validated_data.get('priority'):
            instance.priority = validated_data.get('priority')
        if validated_data.get('status'):
            instance.status = validated_data.get('status')
        if validated_data.get('assignee_user_id'):
            instance.assignee_user_id = validated_data.get('assignee_user_id')
        instance.save()
        return instance

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'created_time', 'description', 'author_user_id']
    
    @transaction.atomic
    def create(self, data, *args, **kwargs):
        author = self.context.get('request').user
        issue = self.context.get('issue')
        comment = Comment.objects.create(**data, author_user_id=author, issue_id=issue)
        comment.save()
        return comment
    
    @transaction.atomic
    def update(self, instance, validated_data):
        instance.description = validated_data.get('description')
        instance.save()
        return instance