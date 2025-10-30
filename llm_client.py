import torch
from config import (
    LLM_MODEL_NAME,
    TRUST_REMOTE_CODE,
    MAX_TOKENS,
    TEMPERATURE,
    BACKEND,  # "vllm" or "transformers")
)

# backend별 모듈 import
if BACKEND == "vllm":
    from vllm import LLM, SamplingParams
elif BACKEND == "transformers":
    from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
else:
    raise ValueError(f"Unsupported BACKEND: {BACKEND}")

# 전역 인스턴스
_llm_instance = None
_tokenizer = None
_pipeline = None


def get_llm_instance():
    """
    싱글톤 패턴으로 LLM 인스턴스를 가져옵니다.
    """
    global _llm_instance, _tokenizer, _pipeline

    if BACKEND == "vllm":
        if _llm_instance is None:
            print(f"[Backend: vLLM] Loading model: {LLM_MODEL_NAME}...")
            _llm_instance = LLM(
                model=LLM_MODEL_NAME,
                trust_remote_code=TRUST_REMOTE_CODE,
            )
            print("vLLM model loaded successfully!")
        return _llm_instance

    elif BACKEND == "transformers":
        if _pipeline is None:
            print(f"[Backend: Transformers] Loading model: {LLM_MODEL_NAME}...")
            _tokenizer = AutoTokenizer.from_pretrained(
                LLM_MODEL_NAME, trust_remote_code=TRUST_REMOTE_CODE
            )
            model = AutoModelForCausalLM.from_pretrained(
                LLM_MODEL_NAME,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto",
                trust_remote_code=TRUST_REMOTE_CODE,
            )
            _pipeline = pipeline(
                "text-generation",
                model=model,
                tokenizer=_tokenizer,
                device=0 if torch.cuda.is_available() else -1,
            )
            print("Transformers model loaded successfully!")
        return _pipeline


def call_llm(prompt, max_tokens=None, temperature=None):
    """
    LLM 호출 (vLLM 또는 Transformers 백엔드 자동 분기)
    """
    if max_tokens is None:
        max_tokens = MAX_TOKENS
    if temperature is None:
        temperature = TEMPERATURE

    try:
        if BACKEND == "vllm":
            llm = get_llm_instance()
            sampling_params = SamplingParams(
                max_tokens=max_tokens,
                temperature=temperature,
            )
            outputs = llm.generate([prompt], sampling_params)
            output = outputs[0].outputs[0]
            prompt_tokens = len(prompt.split())
            completion_tokens = len(output.text.split())

            return {
                "text": output.text,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens,
            }

        elif BACKEND == "transformers":
            pipe = get_llm_instance()
            result = pipe(prompt, max_new_tokens=max_tokens, temperature=temperature)
            text = result[0]["generated_text"]

            prompt_tokens = len(prompt.split())
            completion_tokens = len(text.split()) - prompt_tokens

            return {
                "text": text,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens,
            }

    except Exception as e:
        raise Exception(f"LLM call failed: {str(e)}")


def call_llm_batch(prompts, max_tokens=None, temperature=None):
    """
    여러 프롬프트를 배치로 처리
    """
    if max_tokens is None:
        max_tokens = MAX_TOKENS
    if temperature is None:
        temperature = TEMPERATURE

    try:
        if BACKEND == "vllm":
            llm = get_llm_instance()
            sampling_params = SamplingParams(
                max_tokens=max_tokens,
                temperature=temperature,
            )
            outputs = llm.generate(prompts, sampling_params)
            return [o.outputs[0].text for o in outputs]

        elif BACKEND == "transformers":
            pipe = get_llm_instance()
            results = pipe(prompts, max_new_tokens=max_tokens, temperature=temperature)
            return [r[0]["generated_text"] for r in results]

    except Exception as e:
        raise Exception(f"LLM batch call failed: {str(e)}")
