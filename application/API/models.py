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
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    contributors = models.ManyToManyField(User, through='Contributor', related_name='contributions')

class Contributor(models.Model):
    class ContributorType(models.TextChoices):
        AUTHOR = 'A'
        CONTRIBUTOR = 'C'

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=30, blank=True, null=True)
    permission = models.CharField(max_length=20, choices=ContributorType.choices, default=ContributorType.CONTRIBUTOR)

    class Meta:
        unique_together = ('user_id', 'project_id')

class Issue(models.Model):
    class Tagtype(models.TextChoices):
        BUG = 'B',
        AMELIORATION = 'A',
        TACHE = 'T'
    
    class PriorityType(models.TextChoices):
        FAIBLE = 'F'
        MOYENNE = 'M'
        ELEVEE = 'E'

    class StatusType(models.TextChoices):
        A_FAIRE = 'TODO'
        EN_COURS = 'IN_PROGRESS'
        TERMINE = 'DONE'

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True)
    tag = models.CharField(max_length=20, choices=Tagtype.choices)
    priority = models.CharField(max_length=20, choices=PriorityType.choices)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=StatusType.choices)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author', blank=True, null=True)
    assignee_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignee', blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    description = models.CharField(max_length=1000)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    issue_id = models.ForeignKey(Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
