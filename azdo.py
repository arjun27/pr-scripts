import sys
import json
import requests
from requests.auth import HTTPBasicAuth
from common import *


def parse_pr(instance, project, repo_id, pr_json, user, pwd):
    created_at = pr_json['creationDate']
    pr_id = pr_json['pullRequestId']
    threads = get_prs_threads(instance, project, repo_id, pr_id, user, pwd)
    diff = None

    if threads:
        first_thread = threads[0]
        submitted_at = first_thread['publishedDate']
        diff = diff_seconds(submitted_at, created_at)

    return pr_id, diff


def is_review_thread(thread_json):
    props = thread_json.get('properties')

    if props:
        thread_type = props.get('CodeReviewThreadType')

        if thread_type:
            value = thread_type.get('$value')
            return value == 'VoteUpdate'


def get_prs_threads(instance, project, repo_id, pr_id, user, pwd):
    r = requests.get(
        f'https://{instance}/{project}/_apis/git/repositories/{repo_id}/pullrequests/{pr_id}/threads?api-version=5.0',
        auth=HTTPBasicAuth(user, pwd)
    )
    threads = r.json()
    return list(filter(is_review_thread, threads['value']))


def get_prs(instance, project, repo_id, user, pwd):
    r = requests.get(
        f'https://{instance}/{project}/_apis/git/repositories/{repo_id}/pullrequests?api-version=5.0&searchCriteria.status=completed',
        auth=HTTPBasicAuth(user, pwd)
    ) # filtered to completed only
    return r.json()['value']


if __name__ == "__main__":
    # Example: python azdo.py devdiv.visualstudio.com devdiv <REPO> <USER> <TOKEN>
    instance = sys.argv[1]
    project = sys.argv[2]
    repo = sys.argv[3]
    user = sys.argv[4]
    pwd = sys.argv[5]
    prs = get_prs(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    parsed = list(map(lambda x: parse_pr(sys.argv[1], sys.argv[2], sys.argv[3], x, sys.argv[4], sys.argv[5]), prs))
    show_results(parsed)
