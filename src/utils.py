import requests

MAX_QUERY_ATTEMPTS = 10

def query_runner(query: str, token: str, attemp=1) -> dict:
    """
    This function runs a query against the GitHub GraphQL API and returns the result.
    """
    url = 'https://api.github.com/graphql'
    headers = {'Authorization': 'Bearer {}'.format(token)}
    response = requests.post(url, json={'query': query}, headers=headers)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 502 and attemp <= MAX_QUERY_ATTEMPTS:
        print('Attemp {}/{} get Error 502. Retrying...'.format(attemp, MAX_QUERY_ATTEMPTS))
        return query_runner(query, token, attemp + 1)
    elif response.status_code == 502 and attemp > MAX_QUERY_ATTEMPTS:
        print('Error 502. Maximum number of attempts reached. Try again later.')
        exit(1)
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))
