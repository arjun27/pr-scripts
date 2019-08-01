import requests
import arrow
import sys
import numpy as np
import humanize
import datetime
from common import *


def parse_pr(org, repo, pr_json, token):
    created_at = pr_json['created_at']
    reviews = get_reviews(org, repo, pr_json['number'], token)
    diff = None

    if reviews:
        first_review = reviews[0] # returned in chronological order
        submitted_at = first_review['submitted_at']
        diff = diff_seconds(submitted_at, created_at)

    return pr_json['number'], diff


def get_reviews(org, repo, pr, token):
    r = requests.get(f'https://api.github.com/repos/{org}/{repo}/pulls/{pr}/reviews', headers={'Authorization': f'token {token}'})
    return r.json()


def get_prs(org, repo, token):
    prs = []
    r = requests.get(f'https://api.github.com/repos/{org}/{repo}/pulls?state=closed', headers={'Authorization': f'token {token}'})
    prs.extend(r.json())
    next_url = r.links['next']['url']
    r = requests.get(next_url, headers={'Authorization': f'token {token}'})
    prs.extend(r.json())
    next_url = r.links['next']['url']
    r = requests.get(next_url, headers={'Authorization': f'token {token}'})
    prs.extend(r.json())
    return filter(lambda x: x['user']['type'] != 'Bot', prs) # only return PRs from users, not bots


if __name__ == "__main__":
    # Eg: python github.py microsoft vscode <TOKEN>
    org = sys.argv[1]
    repo = sys.argv[2]
    token = sys.argv[3]
    prs = get_prs(org, repo, token)
    parsed = list(map(lambda x: parse_pr(org, repo, x, token), prs))
    show_results(parsed)
