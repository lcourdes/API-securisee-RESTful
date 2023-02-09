from django.db import models
from authentication.models import User

class Project(models.Model):
    class ProjectType(models.TextChoices):
        BACKEND = 'BE'
        FRONTEND = 'FE'
        IOS = 'IOS'
        ANDROID = 'AN'

    title = models.CharField(max_length=200)
    description=models.CharField(max_length=1000, blank=True)
    type=models.CharField(max_length=20, choices=ProjectType.choices)
    author_user_id = models.IntegerField(blank=True, null=True)
    contributors = models.ManyToManyField(User, through='Contributor', related_name='contributions')

class Contributor(models.Model):
    class ContributorType(models.TextChoices):
        AUTHOR = 'A'
        CONTRIBUTOR = 'C'

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=30)
    permission = models.CharField(max_length=20, choices=ContributorType.choices, default=ContributorType.CONTRIBUTOR)

    class Meta:
        unique_together = ('user_id', 'project_id')
