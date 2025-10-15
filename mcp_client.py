# mcp_client.py

import os
from src.find_file import find_buggy_files
from src.find_FL import FaultLocalizer
from src.fix_code import CodeFixer
from src.test_fix import run_tests
from config import INPUT_DIR, OUTPUT_DIR

def main():
    # Step 1: Find buggy files
    buggy_files = find_buggy_files(INPUT_DIR)
    print(f"Found buggy files: {buggy_files}")

    # Step 2: Localize faults in the buggy files
    fault_localizer = FaultLocalizer()
    fault_locations = {}
    for file in buggy_files:
        faults = fault_localizer.localize_faults(file)
        fault_locations[file] = faults
        print(f"Faults in {file}: {faults}")

    # Step 3: Generate fixes for the identified faults
    code_fixer = CodeFixer()
    fixes = {}
    for file, faults in fault_locations.items():
        fix = code_fixer.generate_fix(file, faults)
        fixes[file] = fix
        print(f"Generated fix for {file}: {fix}")

    # Step 4: Run tests on the fixed code
    test_results = run_tests(OUTPUT_DIR)
    print(f"Test results: {test_results}")

if __name__ == "__main__":
    main()