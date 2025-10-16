import os

def find_buggy_files(directory):
    """
    Find all files in the directory (모든 파일이 버그 파일).
    
    Args:
        directory (str): Directory to search
        
    Returns:
        list: List of file paths
    """
    buggy_files = []
    
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return buggy_files
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            buggy_files.append(file_path)
    
    return buggy_files