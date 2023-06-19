import os
from radon.complexity import cc_visit
from radon.metrics import mi_visit

def calculate_code_complexity(folder_path):
    complexity_results = {}

    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename != 'README.md':
                file_path = os.path.join(dirpath, filename)

                with open(file_path, 'rb') as file:
                    try:
                        code = file.read().decode('utf-8')

                        complexity = cc_visit(code)
                        maintainability_index = mi_visit(code, True)

                        complexity_results[file_path] = {
                            'complexity': complexity,
                            'maintainability_index': maintainability_index
                        }
                        return complexity_results
                    except UnicodeDecodeError:
                        print(f"Skipping file due to null bytes: {file_path}")
                        continue
                return []

    

