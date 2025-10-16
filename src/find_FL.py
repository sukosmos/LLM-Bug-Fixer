from src.file_utils import read_file

class FaultLocalizer:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def localize_faults(self, file_path):
        """
        Analyze a file to localize potential faults using LLM.
        """
        code = read_file(file_path)
        if code is None:
            return {'faults': [], 'tokens': {}}
        
        # 개선된 프롬프트
        prompt = f"""Analyze the following Java code and identify potential bugs.

Code:
{code}

Instructions:
- List each fault on a new line
- Format: "Line X: [brief description]"
- Focus on logical errors, missing returns, type mismatches, etc.
- Do NOT use markdown formatting
- Example format:
  Line 5: Method returns wrong value
  Line 12: Missing return statement

Faults:
"""
        
        try:
            response = self.llm_client(prompt)
            faults = self._parse_fault_response(response['text'])
            
            fl_result = {
                'faults': faults,
                'tokens': response
            }
            
            return fl_result
        except Exception as e:
            print(f"Error calling LLM for fault localization: {e}")
            return {'faults': [], 'tokens': {}}
    
    def _parse_fault_response(self, response):
        faults = []
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            # "Line X:" 형식 찾기
            if line.startswith('Line') and ':' in line:
                faults.append(line)
        
        # 아무것도 못 찾으면 전체 응답 반환
        return faults if faults else [response.strip()]