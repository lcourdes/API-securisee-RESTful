from rest_framework.serializers import ModelSerializer, SerializerMethodField,\
    ValidationError
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
        fields = ['title', 'description', 'type', 'author_user_id',
                  'contributors']

    def get_contributors(self, instance):
        users_queryset = User.objects.filter(contributions=instance)
        serializer = UserShortSerializer(users_queryset, many=True)
        return serializer.data


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['user_id', 'role', 'permission']

    def validate_user_id(self, value):
        project = self.context.get('project')
        user = value.id
        if Contributor.objects.filter(project_id=project,
                                      user_id=user).exists():
            raise ValidationError('This user is already contributing ' +
                                  'to project.')
        return value


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'created_time', 'title', 'description', 'tag',
                  'priority', 'status', 'author_user_id', 'assignee_user_id']

    def validate_assignee_user_id(self, value):
        project = self.context.get('project')
        if not Contributor.objects.filter(project_id=project,
                                          user_id=value.id).exists():
            raise ValidationError('The assignee must be a contributor ' +
                                  'to project.')
        return value


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'created_time', 'description', 'author_user_id']
