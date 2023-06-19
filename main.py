import shutil
from utils.github import clone_repository
from analysis.langchain import load_and_index_files
#from generation.gpt import generate_descriptions
from utils.load_and_index import calculate_code_complexity
from utils.get_repo_name import get_public_repositories

def get_most_complex_repository(user_url):
    # Retrieve user repositories from GitHub API
    repositories = clone_repository(user_url)
    
    # Compute complexity scores for each repository
    # files,file_count = load_and_index_files(repositories)
    # print(files)
    # return file_count
    temp_dict={}
    results = calculate_code_complexity(repositories)
    for file_path, metrics in results.items():
        print(f"File: {file_path}")
        print(f"Cyclomatic Complexity: {str(metrics['complexity'][0]).split(' ')[-1]}")
        print(f"Maintainability Index: {metrics['maintainability_index']}")
        print('-' * 20)
        temp_dict['Cyclomatic Complexity']=str(metrics['complexity'][0]).split(' ')[-1]
        temp_dict['Maintainability Index']=metrics['maintainability_index']/100
        temp_dict['total scor']=int(str(metrics['complexity'][0]).split(' ')[-1]) + metrics['maintainability_index']/100
    return temp_dict
    # Generate descriptions based on complexity scores
    descriptions = generate_descriptions(complexity_scores)
    
    # Find the repository with the highest complexity score
    most_complex_repo = max(complexity_scores, key=complexity_scores.get)
    
    return most_complex_repo, descriptions[most_complex_repo]


def main():
    # user_url = input("Enter the GitHub user's URL: ")
    user_id=input("Enter the GitHub user ID: ")

    
    # Get the most complex repository and its description
    repositories=get_public_repositories(user_id)
    
    if repositories:
        print("Public repositories:")
        for repo in repositories:
            print(repo)
    else:
        print("No public repositories found.")
    # a=get_most_complex_repository(user_url)
    # most_complex_repo, description = get_most_complex_repository(user_url)
    
    # print(f"The most complex repository is: {most_complex_repo}")
    # print(f"Description: {description}")


if __name__ == "__main__":
    main()
