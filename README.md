# GitHub Issues Scraper

A Python script that fetches issue details and associated comments from a specified GitHub repository and saves them to individual text files.

## Features

- Fetches issue details such as number, title, URL, and body content.
- Extracts associated comments of each issue.
- Saves each issue's details in separate text files.
- Skips specific comment text based on defined criteria.

## Requirements

- Python 3.x
- Libraries: `requests`, `BeautifulSoup`

You can install these libraries using pip:

```bash
pip install requests beautifulsoup4
```

## Setup

1. Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

2. Update the `repo_owner`, `repo_name`, and `token` in the script with your desired repository details and personal access token. Ensure you have the necessary permissions to access the repository and its issues.

3. Update the `PATH_TO_EXPORT_TXT_FILES` in the `writeTxt` function to specify where the generated text files should be saved.

## Usage

Run the script:

```bash
python script_name.py
```

## Contribution

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT License](https://choosealicense.com/licenses/mit/)

---

You should replace placeholders like `YOUR_USERNAME`, `YOUR_REPO_NAME`, and `script_name.py` with actual values. Also, if you plan to add more features or require any other libraries in the future, make sure to update the `README.md` accordingly.
