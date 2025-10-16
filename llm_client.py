from vllm import LLM, SamplingParams
from config import LLM_MODEL_NAME, TRUST_REMOTE_CODE, MAX_TOKENS, TEMPERATURE

# 전역 LLM 인스턴스
_llm_instance = None

def get_llm_instance():
    """
    싱글톤 패턴으로 LLM 인스턴스를 가져옵니다.
    """
    global _llm_instance
    if _llm_instance is None:
        print(f"Loading vLLM model: {LLM_MODEL_NAME}...")
        _llm_instance = LLM(
            model=LLM_MODEL_NAME,
            trust_remote_code=TRUST_REMOTE_CODE,
        )
        print("Model loaded successfully!")
    return _llm_instance

def call_llm(prompt, max_tokens=None, temperature=None):
    """
    vLLM 로컬 인스턴스를 사용하여 LLM을 호출합니다.
    
    Returns:
        dict: {
            'text': str (응답 텍스트),
            'prompt_tokens': int (입력 토큰 수),
            'completion_tokens': int (생성 토큰 수),
            'total_tokens': int (총 토큰 수)
        }
    """
    llm = get_llm_instance()
    
    if max_tokens is None:
        max_tokens = MAX_TOKENS
    if temperature is None:
        temperature = TEMPERATURE
    
    sampling_params = SamplingParams(
        max_tokens=max_tokens,
        temperature=temperature
    )
    
    try:
        outputs = llm.generate([prompt], sampling_params)
        output = outputs[0].outputs[0]
        
        # 토큰 수 계산 (근사값)
        prompt_tokens = len(prompt.split())  # 간단한 근사
        completion_tokens = len(output.text.split())
        
        return {
            'text': output.text,
            'prompt_tokens': prompt_tokens,
            'completion_tokens': completion_tokens,
            'total_tokens': prompt_tokens + completion_tokens
        }
    except Exception as e:
        raise Exception(f"LLM call failed: {str(e)}")

def call_llm_batch(prompts, max_tokens=None, temperature=None):
    """
    여러 프롬프트를 배치로 처리합니다.
    
    Args:
        prompts (list): 프롬프트 리스트
        max_tokens (int, optional): 최대 토큰 수
        temperature (float, optional): 샘플링 온도
    
    Returns:
        list: LLM 응답 텍스트 리스트
    """
    llm = get_llm_instance()
    
    if max_tokens is None:
        max_tokens = MAX_TOKENS
    if temperature is None:
        temperature = TEMPERATURE
    
    sampling_params = SamplingParams(
        max_tokens=max_tokens,
        temperature=temperature
    )
    
    try:
        outputs = llm.generate(prompts, sampling_params)
        return [output.outputs[0].text for output in outputs]
    except Exception as e:
        raise Exception(f"LLM batch call failed: {str(e)}")