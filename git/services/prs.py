from django.http import HttpResponse
# DJANGO DB
from django.db import connection
from django.db.utils import OperationalError, IntegrityError
# GIT MODELS
from git.models import PullRequestWait, PullRequest
# TIME LIBRARIES
from datetime import timedelta
from django.utils import timezone


# PULL REQUEST WAIT
def get_lastweek_pr_waits(owner, name):
    with connection.cursor():
        try:
            today = timezone.now().date()
            last_week = today - timedelta(days=7)
            prs = PullRequestWait.objects.all().filter(repo__owner=owner, repo__name=name,
                                                       created_at__lt=today, created_at__gte=last_week)
            return prs
        except (OperationalError, IntegrityError):
            print("DB ERROR")
            return HttpResponse('DB ERROR')


def get_pr_waits_by_month(owner, name, month):
    with connection.cursor():
        try:
            prs = PullRequestWait.objects.all().filter(repo__owner=owner, repo__name=name,
                                                       created_at__month=month, created_at__year=2021).values()
            return list(prs)
        except (OperationalError, IntegrityError):
            print("DB ERROR")
            return HttpResponse('DB ERROR')


def get_lastyear_pr_waits(owner, name):
    with connection.cursor():
        try:
            today = timezone.now().date()
            last_year = today - timedelta(days=365)
            prs = PullRequestWait.objects.all().filter(repo__owner=owner, repo__name=name,
                                                       created_at__lte=today, created_at__gte=last_year).values()
            return list(prs)
        except (OperationalError, IntegrityError):
            print("DB ERROR")
            return HttpResponse('DB ERROR')


def pr_wait_add(repo, number, created_at, merged_at, updated_at, closed_at, merged):
    with connection.cursor():
        try:
            obj = PullRequestWait.objects.get_or_create(repo_id=repo, number=number, created_at=created_at,
                                                        merged_at=merged_at, updated_at=updated_at,
                                                        closed_at=closed_at, merged=merged)
            return obj
        except (OperationalError, IntegrityError):
            print("DB ERROR")
            return HttpResponse('DB ERROR')


# PULL REQUEST
def get_last_week_prs(owner, name):
    with connection.cursor():
        try:
            today = timezone.now().date()
            last_week = today - timedelta(days=7)
            prs = PullRequest.objects.all().filter(repo__owner=owner, repo__name=name,
                                                   created_at__lte=today, created_at__gte=last_week).values()
            return list(prs)
        except (OperationalError, IntegrityError):
            print("DB ERROR")
            return HttpResponse('DB ERROR')


def pr_add(repo, number, created_at, add, delete, commits, merged):
    with connection.cursor():
        try:
            obj = PullRequest.objects.get_or_create(repo_id=repo, number=number, created_at=created_at,
                                                    additions=add, deletions=delete, commits=commits,
                                                    merged=merged)
            return obj
        except (OperationalError, IntegrityError):
            print("DB ERROR")
            return HttpResponse('DB ERROR')
