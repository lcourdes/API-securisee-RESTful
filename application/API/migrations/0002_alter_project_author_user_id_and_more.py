# Generated by Django 4.1.6 on 2023-02-09 11:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('API', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='author_user_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='contributors',
            field=models.ManyToManyField(related_name='contributions', through='API.Contributor', to=settings.AUTH_USER_MODEL),
        ),
    ]
