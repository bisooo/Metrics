from __future__ import absolute_import, unicode_literals
from celery import shared_task
# GIT API LIBRARY SERVICES
from git.services.git import GitWrapper as git


@shared_task
def lastyear_prs(token, owner, name):
    check = git(token).get_lastyear_prs(owner, name)
    if check:
        print("COLLECTED & STORED LAST YEARS PRs for " + owner + "/" + name)
    else:
        print("FAILED TO COLLECT / STORE LAST YEARS PRs for " + owner + "/" + name)
    return check

