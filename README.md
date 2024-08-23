# GitHub Pull Request Analysis Tool

## Overview
This tool fetches and analyzes pull request data from a specified GitHub repository, providing insights into:
- Weekly pull request activity (opened/closed).
- Pull requests stuck in review.
- Complexity of pull requests based on the number of changed files.

## Setup

### Prerequisites
- Python 3.x
- GitHub Personal Access Token (PAT) with `repo` permissions.

### Installation

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd github_pr_tool
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the tool using the following command:
```bash
python pr_tool.py <repository> <token>
