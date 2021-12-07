from __future__ import absolute_import, unicode_literals
from celery import shared_task
# GIT API LIBRARY SERVICES
from git.services.git import GitWrapper as git
# USER SERVICES
from git.services.user import get_user_by_username
# REPOSITORY SERVICES
from git.services.repo import get_repos_watched


@shared_task
def lastyear_pr_waits(token, owner, name):
    print("COLLECTING LAST YEARS PR WAITS for " + owner + "/" + name)
    check = git(token).get_lastyear_pr_waits(owner, name)
    if check:
        print("COLLECTED & STORED LAST YEARS PR WAITS for " + owner + "/" + name)
    else:
        print("FAILED TO COLLECT / STORE LAST YEARS PR WAITS for " + owner + "/" + name)
    lastweek_prs.delay(token, owner, name)
    return check


@shared_task
def lastweek_prs(token, owner, name):
    print("COLLECTING LAST WEEKS PRs for " + owner + "/" + name)
    check = git(token).get_lastweek_prs(owner, name)
    if check:
        print("COLLECTED & STORED LAST WEEKS PRs for " + owner + "/" + name)
    else:
        print("FAILED TO COLLECT / STORE LAST WEEKS PRs for " + owner + "/" + name)
    return check


@shared_task
def update_prs():
    user = get_user_by_username("bisooo")
    repos = get_repos_watched()
    for repo in repos:
        print("UPDATING LAST YEARS PR WAITS for " + repo['repo__owner'] + "/" + repo['repo__name'])
        lastyear_pr_waits.delay(user.token, repo['repo__owner'], repo['repo__name'])
    print("UPDATED ALL WATCHED REPOS PRs")





