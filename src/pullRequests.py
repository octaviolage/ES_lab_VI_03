from datetime import datetime as dt

import pandas as pd

import src.queries as queries
from src.utils import query_runner


OUTPUT = 'out/pullRequests.csv'

def filter_review_time(x):
    """
    This function filters pull requests that have at least an hour in review.
    """
    print(type(x))
    exit(0)
    created_at = dt.strptime(x['createdAt'], '%Y-%m-%dT%H:%M:%SZ')
    closed_at = dt.strptime(x['closedAt'], '%Y-%m-%dT%H:%M:%SZ')
    return (closed_at - created_at).total_seconds() > 3600


def get_pull_requests(nameWithOwner: str, output: pd.DataFrame, token: str):
    """
    This function returns the pull requests data of a repository.
    """
    after = 'null'
    owner, name = nameWithOwner.split('/')
    while True:
        query = queries.pull_requests.replace('{owner}', owner)\
                                     .replace('{name}', name)\
                                     .replace('{after}', after)
        results = query_runner(query, token)
        for pr in results['data']['repository']['pullRequests']['nodes']:
            output = output.append({
                'nameWithOwner': nameWithOwner,
                'id': pr['id'],
                'title': pr['title'],
                'state': pr['state'],
                'createdAt': pr['createdAt'],
                'closedAt': pr['closedAt'],
                'changedFiles': pr['changedFiles'],
                'additions': pr['additions'],
                'deletions': pr['deletions'],
                'reviews': pr['reviews']['totalCount'],
                'body': pr['body'],
                'participants': pr['participants']['totalCount'],
                'comments': pr['comments']['totalCount']
            }, ignore_index=True)
        after = '"' + results['data']['repository']['pullRequests']['pageInfo']['endCursor'] + '"'
        if not results['data']['repository']['pullRequests']['pageInfo']['hasNextPage']:
            break

    # Filter pull requests that have at least a review.
    output = output[output['reviews'] > 0]
    # Filter pull requests that have more than an hour to review.
    output = output[output.apply(filter_review_time, axis=1)]
    return output


def generate_csv(input: str, token: str):
    """
    This function generates a CSV file with the selected pull requests from a file.
    """
    input = pd.read_csv(input)
    output = pd.DataFrame(columns=['nameWithOwner', 'id', 'title', 'state', 'createdAt',
        'closedAt', 'changedFiles', 'additions', 'deletions', 'reviews', 'body',
        'participants', 'comments'])
    for index, row in input.iterrows():
       get_pull_requests(row['nameWithOwner'], output, token)
    output.to_csv(OUTPUT, index=False)
    return OUTPUT



