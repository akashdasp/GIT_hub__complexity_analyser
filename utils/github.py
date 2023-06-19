import os
import subprocess

def clone_repository(repo_url):
    # Create the target folder if it doesn't exist
    target_folder= "temp\\"+ repo_url.split('.')[-2].split('/')[-1]
    os.makedirs(target_folder, exist_ok=True)
    
    # Clone the repository
    try:
        subprocess.run(['git', 'clone', repo_url, target_folder])
        print(f"Repository cloned successfully at: {target_folder}")
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
    return target_folder

# Example usage
# repo_url = 'https://github.com/akashdasp/Mp3_to_Wav_converter.git'
# temp_folder=repo_url.split('.')[-2].split('/')[-1]
# target_folder =temp_folder  # Replace with the desired target folder path

# clone_repository(repo_url)
