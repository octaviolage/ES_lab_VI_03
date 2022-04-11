from os import environ

import src.repositories as repos
import src.pullRequests as prs


def main(num_repos: int, token: str):
    """
    Run the pipeline.
    """
    print('Generating repositories CSV...')
    out_pathname = repos.generate_csv(num_repos, token)
    print('Generating pullRequests CSV...')
    prs.generate_csv(out_pathname, token)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate a CSV file with the most popular repositories on GitHub.')
    parser.add_argument('-n', '--num_repos', type=int, default=100, help='Number of repositories to generate.')
    parser.add_argument('-t', '--token', type=str, default=environ.get('GITHUB_TOKEN'), help='GitHub token.')

    args = parser.parse_args()
    if not args.token:
        print('You must provide a GitHub token or set GITHUB_TOKEN as an environment variable.')
        exit(1)
    main(args.num_repos, args.token)
