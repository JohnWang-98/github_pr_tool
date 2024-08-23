import requests
import argparse
import datetime
from collections import defaultdict

# Function to authenticate and fetch PR data
def fetch_pull_requests(repo, token):
    url = f"https://api.github.com/repos/{repo}/pulls?state=all&per_page=100"
    headers = {"Authorization": f"token {token}"}
    pr_data = []
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")
        pr_data.extend(response.json())
        url = response.links.get('next', {}).get('url')  # Pagination
    return pr_data

# Function to calculate PR metrics
def calculate_metrics(pr_data):
    open_closed_by_week = defaultdict(lambda: {'opened': 0, 'closed': 0})
    stuck_prs = []
    complex_prs = []
    now = datetime.datetime.now()

    for pr in pr_data:
        created_at = datetime.datetime.strptime(pr['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        week = created_at.strftime('%Y-%W')

        open_closed_by_week[week]['opened'] += 1
        if pr['closed_at']:
            closed_at = datetime.datetime.strptime(pr['closed_at'], '%Y-%m-%dT%H:%M:%SZ')
            open_closed_by_week[week]['closed'] += 1
        else:
            if (now - created_at).days > 7:
                stuck_prs.append(pr)

        # Assuming PR size can be gauged by the number of changed files
        if pr['changed_files'] > 20:  # Arbitrary threshold for "complex" PR
            complex_prs.append(pr)

    return open_closed_by_week, stuck_prs, complex_prs

# Function to display results
def display_results(open_closed_by_week, stuck_prs, complex_prs):
    print("\nPull Requests Opened/Closed by Week:")
    for week, counts in sorted(open_closed_by_week.items()):
        print(f"  Week {week}: {counts['opened']} opened, {counts['closed']} closed")

    print("\nStuck Pull Requests (in review for more than 7 days):")
    for pr in stuck_prs:
        print(f"  PR #{pr['number']} - {pr['title']} (created at {pr['created_at']})")

    print("\nComplex Pull Requests (more than 20 files changed):")
    for pr in complex_prs:
        print(f"  PR #{pr['number']} - {pr['title']} ({pr['changed_files']} files changed)")

# Main function to run the tool
def main():
    parser = argparse.ArgumentParser(description="GitHub Pull Request Analysis Tool")
    parser.add_argument("repository", help="GitHub repository in the format 'owner/repo'")
    parser.add_argument("token", help="GitHub Personal Access Token")
    args = parser.parse_args()

    pr_data = fetch_pull_requests(args.repository, args.token)
    open_closed_by_week, stuck_prs, complex_prs = calculate_metrics(pr_data)
    display_results(open_closed_by_week, stuck_prs, complex_prs)

if __name__ == "__main__":
    main()
