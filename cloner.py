#pip install gitpython
from git import Repo
from git import Git
import requests
import os.path
import argparse
from os import path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Easily clone all repositories from server.')
    parser.add_argument('--workdir', type=str, help='Directory to clone projects', required=True)
    parser.add_argument('--token',type=str, help='Gitlab token to authenticate')
    parser.add_argument('--url', type=str, help='Gitlab url')
    
    args = parser.parse_args()

    page = 1
    payload = {'access_token': args.token, 'per_page': '100', 'pagination': 'keyset'}
    while True:
        print 'Requesting page ' + str(page)
        payload['page'] = page
        response = requests.get(args.url + '/api/v4/projects', params = payload)
        total_pages = int(response.headers['X-Total-Pages'])
        for repo in response.json():
            if path.exists(args.workdir + repo['name']):
                print repo['name'] + ' already exists'
                continue
            tags = requests.get(args + '/api/v4/projects/' + str(repo['id']) + '/repository/tags?access_token=' + token).json()
            print 'Getting tags of ' + repo['name']
            if 'message' in tags:
                print 'We couldnt find any projects matching ' + repo['name']
                continue
            for tag in tags:
                rp = Repo.clone_from(repo['http_url_to_repo'], args.workdir + repo['name'] + path.sep + tag['name'])
                Git(rp.working_dir).checkout(tag['name'])
                print 'Cloning ' + repo['name'] + path.sep + tag['name']
        if page == total_pages:
            break
        page = page + 1