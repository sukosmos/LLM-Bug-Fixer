# main.py
"""
LLM Bug Fixer Pipeline
=====================
Automated bug fixing pipeline using LLM:
1. Fault Localization (FL)
2. Code Fix Generation
3. Test Validation
"""

import os
import json
from datetime import datetime
from src.file_utils import get_all_files
from src.find_FL import FaultLocalizer
from src.fix_code import CodeFixer
from src.test_fix import run_tests
from config import INPUT_DIR, LOGS_OUTPUT_DIR
from llm_client import call_llm

def main():
    print("=" * 80)
    print("Starting Bug Fixing Pipeline with vLLM Local Instance")
    print("=" * 80)
    
    # 시작 시간 기록
    start_time = datetime.now()
    
    # 전체 토큰 사용량 추적
    total_tokens = {
        'prompt_tokens': 0,
        'completion_tokens': 0,
        'total_tokens': 0
    }
    
    # Step 1: Get all buggy files
    print("\n[Step 1] Loading buggy files...")
    buggy_files = get_all_files(INPUT_DIR, extension='.java')
    
    if not buggy_files:
        print(f"No Java files found in {INPUT_DIR}")
        print("Please check if the directory exists and contains .java files")
        return
    
    print(f"Found {len(buggy_files)} Java file(s):")
    for f in buggy_files:
        print(f"  - {os.path.basename(f)}")

    # Step 2 & 3: FL and Fix for each file
    print("\n[Step 2 & 3] Fault Localization and Fix Generation...")
    fault_localizer = FaultLocalizer(call_llm)
    code_fixer = CodeFixer(call_llm)
    
    # 각 파일의 FL, Fix 결과 저장
    file_results = {}
    
    for file in buggy_files:
        filename = os.path.basename(file)
        print(f"\n  Processing: {filename}")
        
        # Fault Localization
        print(f"    → Localizing faults...")
        fl_result = fault_localizer.localize_faults(file)
        fl_tokens = fl_result.get('tokens', {})
        
        # 토큰 누적
        total_tokens['prompt_tokens'] += fl_tokens.get('prompt_tokens', 0)
        total_tokens['completion_tokens'] += fl_tokens.get('completion_tokens', 0)
        total_tokens['total_tokens'] += fl_tokens.get('total_tokens', 0)
        
        print(f"    → Faults found: {len(fl_result.get('faults', []))}")
        
        # Fix Generation
        print(f"    → Generating fix...")
        fix_result = code_fixer.generate_fix(file, fl_result)
        fix_tokens = fix_result.get('tokens', {})
        
        # 토큰 누적
        total_tokens['prompt_tokens'] += fix_tokens.get('prompt_tokens', 0)
        total_tokens['completion_tokens'] += fix_tokens.get('completion_tokens', 0)
        total_tokens['total_tokens'] += fix_tokens.get('total_tokens', 0)
        
        # 결과 저장
        file_results[file] = {
            'fl_result': fl_result,
            'fix_result': fix_result
        }

    # Step 4: Run tests on all fixed code
    print("\n[Step 4] Running tests...")
    fixed_files_info = {
        file: results['fix_result'] 
        for file, results in file_results.items()
    }
    test_results = run_tests(fixed_files_info)
    
    # Step 5: Save complete results (FL + Fix + Test) to JSON files
    print("\n[Step 5] Saving complete results...")
    for file, results in file_results.items():
        filename = os.path.basename(file)
        test_result = test_results.get(filename, {
            'compiled': False,
            'tests_run': 0,
            'passed': 0,
            'failed': 0,
            'errors': ['Test not executed']
        })
        
        code_fixer.save_complete_result(
            file,
            results['fl_result'],
            results['fix_result'],
            test_result
        )
    
    # 콘솔 로그 저장
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    log_path = os.path.join(LOGS_OUTPUT_DIR, f'pipeline_{start_time.strftime("%Y%m%d_%H%M%S")}.log')
    log_content = f"""Bug Fixing Pipeline Execution Log
================================================================================
Start Time: {start_time.isoformat()}
End Time: {end_time.isoformat()}
Duration: {duration:.2f} seconds

Files Processed: {len(buggy_files)}
Total Tokens Used: {total_tokens['total_tokens']}
  - Prompt Tokens: {total_tokens['prompt_tokens']}
  - Completion Tokens: {total_tokens['completion_tokens']}

Results saved to: output/fixes/
================================================================================
"""
    
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(log_content)
    
    print("\n" + "=" * 80)
    print("Bug Fixing Pipeline Completed!")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Total tokens used: {total_tokens['total_tokens']}")
    print(f"Complete results saved to: output/fixes/")
    print(f"Log saved to: {log_path}")
    print("=" * 80)

if __name__ == "__main__":
    main()