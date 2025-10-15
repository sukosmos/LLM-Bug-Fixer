def call_llm(prompt, model_name="your-model-name"):
    import requests

    # vLLM OpenAI 호환 API 엔드포인트
    url = "http://localhost:8000/v1/completions"
    headers = {"Content-Type": "application/json"}
    
    data = {
        "model": model_name,
        "prompt": prompt,
        "max_tokens": 2000,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["text"]
        else:
            raise Exception(f"LLM call failed with status code {response.status_code}: {response.text}")
    except requests.exceptions.ConnectionError:
        raise Exception("LLM 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")