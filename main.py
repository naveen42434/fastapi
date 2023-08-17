import json
from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def root():
    return {"status": "OK"}

@app.get("/github/{orgname}/{repo}/{branchname}")
def github(orgname: str, repo: str, branchname: str, authtoken: str):
    url = f"https://api.github.com/repos/{orgname}/{repo}/git/refs?authtoken={authtoken}"
    response = requests.get(url)
    data = response.json()

    if isinstance(data, list) and len(data) > 0:
        s = data[0].get("object", {}).get("sha")
        url1 = f"https://api.github.com/repos/{orgname}/{repo}/git/refs"
        payload = json.dumps({
            "ref": f"refs/heads/{branchname}",
            "sha": s
        })
        header = {
            'Authorization': f'Token {authtoken}',
            'Content-Type': 'application/json',
            'Cookie': '_octo=GH1.1.1883553354.1686214504; logged_in=no; _octo=GH1.1.1883553354.1686214504; logged_in=no'
        }
        response = requests.post(url1, headers=header, data=payload)
        return response.json()
    else:
        return {"error": "Failed to retrieve data from GitHub API."}

@app.post("/gitlab/{orgname}/{repo}/{branchname}")
def gitlab(orgname:str,repo:str,branchname:str,authtoken:str):
    url = f"https://gitlab.com/api/v4/projects/{orgname}%2F{repo}/repository/branches"

    payload = json.dumps({
        "branch": f"{branchname}",
        "ref": "main"
    })
    headers = {
        'PRIVATE-TOKEN': f"{authtoken}",
        'Content-Type': 'application/json',
        'Cookie': '_cfuvid=hWzksuP.vbDPJy8jlHCWyff2.QGGyeo2drCli6UsLj0-1686308506707-0-604800000; _gitlab_session=bf692d61ac0c4d0ed59bb84277e7dc2f'
    }
    response = requests.post(url, headers=headers, data=payload)

    return response.json()

@app.post("/bitbucket/{workspace}/{repository}/{branchname}")
def bitbucket(workspace:str,repository:str,branchname:str,authtoken:str):
    url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repository}/refs/branches"

    payload = {
        "name": f"{branchname}",
        "target": {
            "hash": "master"
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic "+f"{authtoken}"
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()
