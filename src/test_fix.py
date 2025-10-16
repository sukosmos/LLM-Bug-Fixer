import os
import subprocess
from config import TEST_DIR, FIXES_OUTPUT_DIR

def compile_java_file(java_file):
    """
    Compile a Java file.
    
    Returns:
        bool: True if compilation succeeded, False otherwise
    """
    try:
        result = subprocess.run(
            ['javac', java_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Compilation error: {e}")
        return False

def run_java_tests(test_file, fixed_file):
    """
    Run Java tests for a fixed file.
    
    Returns:
        dict: Test results
    """
    try:
        # Compile fixed file and test file
        compile_success = compile_java_file(fixed_file)
        if not compile_success:
            return {
                'compiled': False,
                'tests_run': 0,
                'passed': 0,
                'failed': 0,
                'errors': ['Compilation failed']
            }
        
        compile_test_success = compile_java_file(test_file)
        if not compile_test_success:
            return {
                'compiled': True,
                'tests_run': 0,
                'passed': 0,
                'failed': 0,
                'errors': ['Test compilation failed']
            }
        
        # Run tests (JUnit)
        test_class = os.path.splitext(os.path.basename(test_file))[0]
        result = subprocess.run(
            ['java', '-cp', f'.:{os.path.dirname(test_file)}:/usr/share/java/junit4.jar', 
             'org.junit.runner.JUnitCore', test_class],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=os.path.dirname(test_file)
        )
        
        # Parse test results
        output = result.stdout + result.stderr
        test_results = {
            'compiled': True,
            'tests_run': 0,
            'passed': 0,
            'failed': 0,
            'errors': [],
            'output': output
        }
        
        # Simple parsing
        if 'OK' in output:
            test_results['passed'] = test_results['tests_run']
        
        return test_results
        
    except Exception as e:
        return {
            'compiled': False,
            'tests_run': 0,
            'passed': 0,
            'failed': 0,
            'errors': [str(e)]
        }

def run_tests(fixed_files_info):
    """
    Run tests for all fixed files.
    
    Args:
        fixed_files_info (dict): Dictionary mapping original files to fix info
        
    Returns:
        dict: Overall test results
    """
    all_results = {}
    
    for original_file, fix_info in fixed_files_info.items():
        filename = os.path.basename(original_file)
        fixed_file = os.path.join(FIXES_OUTPUT_DIR, filename)
        
        # Find corresponding test file
        test_filename = filename.replace('.java', 'Test.java')
        test_file = os.path.join(TEST_DIR, test_filename)
        
        if not os.path.exists(test_file):
            print(f"Warning: Test file not found for {filename}")
            all_results[filename] = {
                'compiled': False,
                'tests_run': 0,
                'passed': 0,
                'failed': 0,
                'errors': ['Test file not found']
            }
            continue
        
        print(f"Running tests for {filename}...")
        test_results = run_java_tests(test_file, fixed_file)
        all_results[filename] = test_results
    
    return all_results
