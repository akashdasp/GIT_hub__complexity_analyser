import subprocess
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from langchain.document_loaders import DirectoryLoader, NotebookLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import uuid
import ast

# def get_duplicate_code_count(project_path):
#     # Run pylint with duplicate-code check
#     cmd = f"pylint --disable=all --enable=duplicate-code {project_path}"
#     result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

#     # Extract duplicate code count from pylint output
#     output = result.stdout
#     count_match = re.search(r"Found (\d+) instances of duplicate code", output)
#     if count_match:
#         duplicate_code_count = int(count_match.group(1))
#         return duplicate_code_count
#     else:
#         return 0

# Example usage


# def count_code_comments(file_path):
#     with open(file_path, "r") as file:
#         code = file.read()

#     tree = ast.parse(code)
#     comments = [node for node in ast.walk(tree) if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str)]

#     return len(comments)


def clean_and_tokenize(text):
    # Replace this function with appropriate text cleaning and tokenization logic using scikit-learn

    # Example using CountVectorizer and TfidfTransformer from scikit-learn
    pipeline = Pipeline([
        ('count_vectorizer', CountVectorizer()),
        ('tfidf_transformer', TfidfTransformer())
    ])
    tokenized_text = pipeline.fit_transform([text])

    return tokenized_text

def load_and_index_files(repo_path):
    extensions = ['txt', 'md', 'markdown', 'rst', 'py', 'js', 'java', 'c', 'cpp', 'cs', 'go', 'rb', 'php', 'scala', 'html', 'htm', 'xml', 'json', 'yaml', 'yml', 'ini', 'toml', 'cfg', 'conf', 'sh', 'bash', 'css', 'scss', 'sql', 'gitignore', 'dockerignore', 'editorconfig', 'ipynb']

    file_type_counts = {}
    documents_dict = {}

    for ext in extensions:
        glob_pattern = f'**/*.{ext}'
        try:
            loader = None
            if ext == 'ipynb':
                loader = NotebookLoader(str(repo_path), include_outputs=True, max_output_length=20, remove_newline=True)
            else:
                loader = DirectoryLoader(repo_path, glob=glob_pattern)

            loaded_documents = loader.load() if callable(loader.load) else []
            if loaded_documents:

                file_type_counts[ext] = len(loaded_documents)
                for doc in loaded_documents:
                    file_path = doc.metadata['source']
                    relative_path = os.path.relpath(file_path, repo_path)
                    file_id = str(uuid.uuid4())
                    doc.metadata['source'] = relative_path
                    doc.metadata['file_id'] = file_id

                    documents_dict[file_id] = doc
        except Exception as e:
            print(f"Error loading files with pattern '{glob_pattern}': {e}")
            continue

    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=200)

    # split_documents = []
    # for file_id, original_doc in documents_dict.items():
    #     split_docs = text_splitter.split_documents([original_doc])
    #     for split_doc in split_docs:
    #         split_doc.metadata['file_id'] = original_doc.metadata['file_id']
    #         split_doc.metadata['source'] = original_doc.metadata['source']

    #     split_documents.extend(split_docs)

    # if split_documents:
    #     tokenized_documents = [clean_and_tokenize(doc.page_content) for doc in split_documents]
    #     index = BM25Okapi(tokenized_documents)
    return file_type_counts,sum(file_type_counts.values()) #,[doc.metadata['source'] for doc in split_documents]



