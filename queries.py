repositories = """
{
  search(query: "stars:>100 sort:stars", type: REPOSITORY, first: 25, after: {after}) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      ... on Repository {
        nameWithOwner
        url
        createdAt
        stargazers {
          totalCount
        }
        prsClosed: pullRequests(states: CLOSED) {
            totalCount
        }
        prsMerged: pullRequests(states: MERGED) {
            totalCount
        }
      }
    }
  }
}
    """

repositories = """
    {
      repository(name: {name}, owner: {owner}) {
        prClosed: pullRequests(states: CLOSED, first: 100, after: {after}) {
          pageInfo {
            endCursor
            hasNextPage
          }
          nodes {
            title
            createdAt
            closedAt
            additions
            deletions
            files { totalCount }
            reviews { totalCount }
            body
            comments { totalCount }
          }
        }
      }
    }
    """