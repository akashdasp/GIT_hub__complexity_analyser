import requests
import openai
from dotenv import load_dotenv
import os
# Set up your OpenAI API credentials
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# Function to analyze repository text and calculate complexity score
def analyze_repository(repository):
    # Concatenate relevant textual information such as name, description, and README
    text = repository['name'] + ' ' + repository['description']
    readme_text = get_readme_text(repository['full_name'])
    if readme_text:
        text += ' ' + readme_text

    # Use OpenAI API for text analysis
    response = openai.Completion.create(
        engine='text-davinci-003',  # Choose the appropriate OpenAI language model
        prompt=text,
        max_tokens=100,
        temperature=0.8,
        n=1,
        stop=None,
    )

    # Extract the complexity score from OpenAI API response
    complexity = response.choices[0].text.strip()

    return complexity

# Function to fetch README text for a given repository
def get_readme_text(repo_full_name):
    url = f"https://api.github.com/repos/{repo_full_name}/readme"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json().get('content', None)
    else:
        return None

# Function to get the most complex repository
def get_most_complex_repository(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)

    if response.status_code == 200:
        repositories = response.json()

        most_complex_repo = None
        max_complexity = float('-inf')

        for repository in repositories:
            complexity = analyze_repository(repository)
            # Convert the complexity score to a numerical value if necessary
            # ...

            if complexity > max_complexity:
                max_complexity = complexity
                most_complex_repo = repository['name']

        return most_complex_repo
    else:
        print(f"Failed to fetch repositories: {response.status_code} - {response.text}")
        return None

# Replace with the GitHub username you want to retrieve public repositories for
username = "akashdasp"

most_complex_repository = get_most_complex_repository(username)
if most_complex_repository:
    print(f"The most complex repository for user {username} is: {most_complex_repository}")
