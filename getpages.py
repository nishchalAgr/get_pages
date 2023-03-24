import requests
import os
from dotenv import load_dotenv, find_dotenv
import sys

def get_pages(name, token):

    get_repo_url = 'https://api.github.com/users/{name}/repos'.format(name=name)
    get_page_url = 'https://api.github.com/repos/{name}/'.format(name=name)

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + token
    }

    res = requests.get(get_repo_url, headers=headers).json()
    arr = []
    for repo in res:
        url = get_page_url + repo['name'] + '/pages'
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            print(res.json()['html_url'])
            arr.append(res.json()['html_url'])
    return arr

if len(sys.argv) == 1:
    print('github username required')
    exit()

load_dotenv(find_dotenv())
get_pages(sys.argv[1], os.getenv('APIKey'))