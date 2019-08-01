import requests
import arrow
import sys
import numpy as np
import humanize
import datetime


def diff_seconds(a, b):
    return (arrow.get(a) - arrow.get(b)).total_seconds()


def hm(secs):
    return humanize.naturaldelta(datetime.timedelta(seconds=secs))


def show_results(parsed):
    print("Number of PRs:", len(parsed))
    times = map(lambda x: x[1], parsed)
    without_none = filter(None, times)
    without_5_seconds = list(filter(lambda x: x > 4, without_none))
    print("Number of reviewed PRs:", len(without_5_seconds))
    print("Median (50th perc), in mins:", hm(np.percentile(without_5_seconds, 50)))
    print("75th percentile, in mins:", hm(np.percentile(without_5_seconds, 25)))
    print("90th percentile, in mins:", hm(np.percentile(without_5_seconds, 10)))
