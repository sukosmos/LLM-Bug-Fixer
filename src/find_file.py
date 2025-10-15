def find_buggy_files(directory):
    import os

    buggy_patterns = ['TODO', 'FIXME', 'bug', 'error']  # Add more patterns as needed
    buggy_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.java'):  # Assuming we're looking for Java files
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if any(pattern in content for pattern in buggy_patterns):
                        buggy_files.append(file_path)

    return buggy_files