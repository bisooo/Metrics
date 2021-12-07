# Generated by Django 3.2.9 on 2021-12-07 10:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='username')),
                ('token', models.CharField(max_length=40, unique=True, verbose_name='token')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'USER',
                'verbose_name_plural': 'USERs',
            },
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=39, verbose_name='repo owner')),
                ('name', models.CharField(max_length=40, verbose_name='repo name')),
                ('url', models.CharField(max_length=180, verbose_name='repo url')),
            ],
            options={
                'verbose_name': 'REPO',
                'verbose_name_plural': 'REPOs',
                'unique_together': {('owner', 'name')},
            },
        ),
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='git.repository')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'WATCH LIST',
                'verbose_name_plural': 'WATCH LISTs',
            },
        ),
        migrations.CreateModel(
            name='PullRequestWait',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField()),
                ('merged_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('closed_at', models.DateTimeField(blank=True, null=True)),
                ('merged', models.BooleanField()),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='git.repository')),
            ],
            options={
                'verbose_name': 'PR WAIT',
                'verbose_name_plural': 'PR WAITs',
                'unique_together': {('repo', 'number')},
            },
        ),
        migrations.CreateModel(
            name='PullRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField()),
                ('additions', models.PositiveIntegerField()),
                ('deletions', models.PositiveIntegerField()),
                ('commits', models.PositiveIntegerField()),
                ('merged', models.BooleanField()),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='git.repository')),
            ],
            options={
                'verbose_name': 'PR',
                'verbose_name_plural': 'PRs',
                'unique_together': {('repo', 'number')},
            },
        ),
    ]
