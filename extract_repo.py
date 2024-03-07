# used to automatically clone git repo
from git import Repo
import requests
import re
import streamlit as st
import os


def parse_repo_url(repo_url):
    """
    Parse the repo url to return username and repo name
    E.g. 'https://github.com/Jaryang/cappyfoodies' --> Jaryang, cappyfoodies
    """

    obj = re.search(r"github\.com/(.+?)/(.+)", repo_url)

    return (obj.group(1), obj.group(2))


def is_repo_public(repo_url):
    """
    Check if a GitHub repository is public.
    Params:
        username: GitHub username or organization name
        repo_name: Name of the repository
    return: 
        True if the repository is public, False if private or not found
    """
    username, repo_name = parse_repo_url(repo_url)
    url = f"https://api.github.com/repos/{username}/{repo_name}"
    response = requests.get(url)
    if response.status_code == 200:
        repo_info = response.json()
        return not repo_info.get('private', True)  # Returns True if not private
    else:
        # Handle errors (e.g., repo not found or access denied)
        return False


@st.cache_data
def get_repo(repo_url, to_dir):
    """
    repo_url (str): the https link of github repo
    to_dir (str): where to store the repo
    """
    username, repo_name = parse_repo_url(repo_url)

    if os.path.exists(to_dir):
        print(f"{to_dir} already exists")

    else:
        if not is_repo_public(repo_url):
            Repo.clone_from(repo_url, to_dir)

        else:
            print("This is a private repo that requires credentials")
            password = st.text_input('Your Password:', 'Note: Your credentials will not be saved and shared')
            new_repo_url = f"https://{username}:{password}@github.com/{username}/{repo_name}.git"
            Repo.clone_from(new_repo_url, to_dir)
    