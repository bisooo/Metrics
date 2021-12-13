from django.http import HttpResponse
# PULL REQUEST WAIT MODEL
from git.models import PullRequestWait
# CSV WRITER
import csv


def export(request):

    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['repo_owner', 'repo_name', 'pr_number', 'created_at', 'merged_at', 'merged'])
    for pr in PullRequestWait.objects.all().values_list('repo__owner', 'repo__name', 'number', 'created_at', 'merged_at', 'merged'):
        writer.writerow(pr)

    response['Content-Disposition'] = 'attachment; filename="prs.csv"'
    return response
