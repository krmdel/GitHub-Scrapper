# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import time

# Function to write issue data to text files
def writeTxt(all_issues_data):
    # Define the path to save the exported text files
    txt_path = 'PATH_TO_EXPORT_TXT_FILES'
    # Loop through each issue's data
    for i in range(len(all_issues_data)):
        # Create or overwrite a text file named after the issue number
        with open(f'{txt_path}/{all_issues_data[i][0]}.txt', 'w', encoding='utf-8') as f:
            # Write the issue details to the file
            f.write(f'Issue number: {all_issues_data[i][0]}\n')
            f.write(f'Title: {all_issues_data[i][1]}\n')
            f.write(f'URL: {all_issues_data[i][2]}\n')
            f.write(f'Body: {all_issues_data[i][3]}\n')
            # Write each comment associated with the issue
            for j in range(len(all_issues_data[i][4])):
                f.write(f'Comment {j}:\n {all_issues_data[i][4][j][0]}\n')

# Function to fetch issue numbers from a GitHub page
def fetch_issue_numbers(url):
    # Define headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    # If the request is successful, parse the HTML and extract issue numbers
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        issue_links = soup.select('a.Link--primary.v-align-middle.no-underline.h4.js-navigation-open.markdown-title')
        issue_numbers = [link['href'].split('/')[-1] for link in issue_links]
        return issue_numbers
    else:
        print(f"Error: {response.status_code}")
        return []

# Function to fetch detailed data of a specific issue using GitHub API
def fetch_issue_details(repo_owner, repo_name, issue_number, token):
    # Define the API endpoint URL
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Function to fetch comments of a specific issue using GitHub API
def fetch_issue_comments(repo_owner, repo_name, issue_number, token):
    # Define the API endpoint URL for comments
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}/comments"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return []

# Function to determine the total number of issue pages for a repository
def get_total_pages(url):
    # Define headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        pagination = soup.select('div.pagination')
        if pagination:
            last_page = int(pagination[0].find_all('a')[-2].text)
            return last_page
    return 1

# Example usage:
# Define repository and token details
repo_owner = "ultralytics"
repo_name = "ultralytics"
token = "YOUR_TOKEN"
# Text to ignore in comments
ignore_text = '''
If this is a 🐛 Bug Report, please provide a [minimum reproducible example](https://docs.ultralytics.com/help/minimum_reproducible_example/) to help us debug it.
'''
# Define the base URL to fetch closed issues
base_url = f"https://github.com/{repo_owner}/{repo_name}/issues?q=is%3Aissue+is%3Aclosed"
total_pages = get_total_pages(base_url)
print(f"Total pages: {total_pages}")

all_issues_data = []
# Loop through each page of issues
for page in range(1, total_pages + 1):
    page_url = f"https://github.com/{repo_owner}/{repo_name}/issues?page={page}&q=is%3Aissue+is%3Aclosed" 
    print(f"Fetching page {page} of {total_pages}")    
    print(page_url)
    issue_numbers = fetch_issue_numbers(page_url)
    # Uncomment to sleep for 2 seconds to avoid rate limit
    # time.sleep(2)
    # Loop through each issue number on the current page
    for issue_number in issue_numbers:
        print(f"Fetching issue #{issue_number}")
        issue_details = fetch_issue_details(repo_owner, repo_name, issue_number, token)
        # Uncomment to sleep for 1 second to avoid rate limit
        # time.sleep(1)
        comments = fetch_issue_comments(repo_owner, repo_name, issue_number, token)
        # Uncomment to sleep for 1 second to avoid rate limit
        # time.sleep(1)
        # Compile issue data
        issue_data = {
            'issue_number': issue_number,
            'title': issue_details['title'],
            'body': issue_details['body'],
            'html_url': issue_details['html_url'],
            'comments': comments
        }
        # Filter out comments containing the ignore text
        comment = []
        for i in range(len(issue_data['comments'])):
            if not ignore_text in issue_data['comments'][i]['body']:
                comment.append([issue_data['comments'][i]['body']])   
        # Append compiled issue data to the main list
        all_issues_data.append([issue_data['issue_number'], issue_data['title'], issue_data['html_url'], issue_data['body'], comment])
    # Write the fetched issues to text files and clear the list for the next batch
    print(f"Writing {len(all_issues_data)} issues from page {page} to file...")
    writeTxt(all_issues_data)
    del all_issues_data[:]
