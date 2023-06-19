import requests

def get_public_repositories(user_id):
    url = f"https://api.github.com/users/{user_id}/repos"
    response = requests.get(url)

    if response.status_code == 200:
        repositories = response.json()
        repository_names = [repo['name'] for repo in repositories]
        return repository_names
    else:
        print(f"Failed to fetch repositories. Error: {response.status_code} - {response.text}")
        return []