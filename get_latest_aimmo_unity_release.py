import urllib
from zipfile import ZipFile
from github import Github
import os

# Access Token with only public access permissions
g = Github(os.environ['GITHUB_API_TOKEN'])

# Accessing aimmo-unity repo by ID.
repo = g.get_repo(96999382)

# Get the latest release
releases = repo.get_releases()
first_release = releases[0]

release_assets = first_release.get_assets()

urllib.urlretrieve(release_assets[0].browser_download_url,
                   'release.zip')

with ZipFile('release.zip', 'r') as zipped_release:
    zipped_release.extractall('lib/players/static/unity/')
