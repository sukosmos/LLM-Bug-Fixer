import os
import json
import re
from config import FIXES_OUTPUT_DIR
from src.file_utils import read_file, write_file


class CodeFixer:
    def __init__(self, llm_client):
        """
        Initialize the CodeFixer with an LLM client.
        """
        self.llm_client = llm_client

    def generate_fix(self, file_path, fl_result):
        """
        Generate a fix for the identified faults using LLM.

        Returns:
            dict: {
                'fixed_code': str,
                'fixed_file': str,
                'tokens': dict
            }
        """
        code = read_file(file_path)
        if code is None:
            return {'fixed_code': None, 'fixed_file': None, 'tokens': {}}

        faults = fl_result.get('faults', [])
        faults_description = '\n'.join(faults)

        # 개선된 프롬프트: 명확한 지시 + 예시 제공
        prompt = f"""Fix the following Java code based on the identified faults.

Original Code:
{code}

Identified Faults:
{faults_description}

Instructions:
- Output ONLY valid Java code that can be compiled directly
- Do NOT use markdown code blocks (no ```)
- Do NOT add explanations before or after the code
- You may add comments (// or /* */) inside the code
- Start with package/import/class declaration immediately

Fixed Code:
"""

        try:
            response = self.llm_client(prompt, max_tokens=4000)
            fixed_code = response['text'].strip()

            # 코드 추출
            fixed_code = self._clean_code(fixed_code)

            # 저장
            filename = os.path.basename(file_path)
            fixed_output_path = os.path.join(FIXES_OUTPUT_DIR, filename)
            write_file(fixed_output_path, fixed_code)

            fix_result = {
                'fixed_code': fixed_code,
                'fixed_file': fixed_output_path,
                'tokens': response
            }

            print(f"    Fixed code saved to: {fixed_output_path}")
            return fix_result
        except Exception as e:
            print(f"    Error generating fix: {e}")
            return {'fixed_code': None, 'fixed_file': None, 'tokens': {}}

    def _clean_code(self, code):
        """
        코드 블록만 추출: 마크다운, 설명문 등을 제거하고 순수 코드만 반환
        """
        # 1. 마크다운 코드 블록 제거
        code = re.sub(r'^```(?:java)?\s*\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'\n```\s*$', '', code, flags=re.MULTILINE)
        
        # 2. 코드 시작 전 설명문 제거 (package/import/public class 이전의 텍스트)
        # Java 코드의 시작점을 찾음
        match = re.search(r'^(package\s+|import\s+|public\s+class\s+|class\s+|public\s+interface\s+|interface\s+|/\*|//)', 
                         code, re.MULTILINE | re.IGNORECASE)
        if match:
            code = code[match.start():]
        
        # 3. 코드 끝 이후 설명문 제거 (마지막 } 이후의 텍스트)
        # 마지막 중괄호를 찾아서 그 이후 텍스트 제거
        lines = code.split('\n')
        last_brace_idx = -1
        for i in range(len(lines) - 1, -1, -1):
            if '}' in lines[i]:
                last_brace_idx = i
                break
        
        if last_brace_idx != -1:
            # 마지막 } 이후 비어있지 않은 라인이 있다면 제거
            code = '\n'.join(lines[:last_brace_idx + 1])
        
        return code.strip()
       
    def save_complete_result(self, file_path, fl_result, fix_result, test_result):
        """
        FL, Fix, Test 결과를 하나의 JSON 파일에 저장합니다.
        """
        filename = os.path.basename(file_path)
        json_output_path = os.path.join(FIXES_OUTPUT_DIR, f"{filename}.json")

        complete_result = {
            'file': filename,
            'original_path': file_path,
            'fl': {
                'faults': fl_result.get('faults', []),
                'token_usage': {
                    'prompt_tokens': fl_result.get('tokens', {}).get('prompt_tokens', 0),
                    'completion_tokens': fl_result.get('tokens', {}).get('completion_tokens', 0),
                    'total_tokens': fl_result.get('tokens', {}).get('total_tokens', 0)
                }
            },
            'fix': {
                'fixed_file': fix_result.get('fixed_file'),
                'token_usage': {
                    'prompt_tokens': fix_result.get('tokens', {}).get('prompt_tokens', 0),
                    'completion_tokens': fix_result.get('tokens', {}).get('completion_tokens', 0),
                    'total_tokens': fix_result.get('tokens', {}).get('total_tokens', 0)
                }
            },
            'test': {
                'compiled': test_result.get('compiled', False),
                'tests_run': test_result.get('tests_run', 0),
                'passed': test_result.get('passed', 0),
                'failed': test_result.get('failed', 0),
                'errors': test_result.get('errors', [])
            }
        }

        with open(json_output_path, 'w', encoding='utf-8') as f:
            json.dump(complete_result, f, indent=2, ensure_ascii=False)

        print(f"    Complete result saved to: {json_output_path}")