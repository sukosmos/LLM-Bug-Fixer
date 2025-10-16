import os

def get_all_files(directory, extension='.java'):
    """
    디렉토리에서 모든 파일을 가져옵니다.
    
    Args:
        directory (str): 파일을 찾을 디렉토리
        extension (str): 파일 확장자 (기본값: .java)
        
    Returns:
        list: 파일 경로 리스트
    """
    files = []
    
    if not os.path.exists(directory):
        print(f"Error: Directory not found: {directory}")
        return files
    
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                files.append(file_path)
    
    return sorted(files)

def read_file(file_path):
    """
    파일 내용을 읽습니다.
    
    Args:
        file_path (str): 파일 경로
        
    Returns:
        str: 파일 내용
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def write_file(file_path, content):
    """
    파일에 내용을 씁니다.
    
    Args:
        file_path (str): 파일 경로
        content (str): 파일 내용
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Error writing file {file_path}: {e}")