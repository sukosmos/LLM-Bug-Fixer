# config.py

import os

# Configuration settings for the bug-fixing pipeline

# hf tokens
# Input and output directories
INPUT_DIR = os.path.join('data', 'target')
TEST_DIR = os.path.join('data', 'test')
OUTPUT_DIR = 'output'
FIXES_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'fixes')
LOGS_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'logs')

# Model parameters - vLLM 로컬 인스턴스
'''
models
[vllm]
- 'LGAI-EXAONE/EXAONE-3.0-7.8B-Instruct' 
- 'upstage/solar-pro-preview-instruct' 22B (x)
- 'naver-hyperclovax/HyperCLOVAX-SEED-Vision-Instruct-3B' (x)


[transformers]
- 'naver-hyperclovax/HyperCLOVAX-SEED-Think-14B' (x)
- 'naver-hyperclovax/HyperCLOVAX-SEED-Text-Instruct-1.5B' 
- 'upstage/SOLAR-10.7B-Instruct-v1.0'
- 'K-intelligence/Midm-2.0-Mini-Instruct'
- 'skt/A.X-4.0-Light'
- 'kakaocorp/kanana-1.5-8b-instruct-2505'
'''
LLM_MODEL_NAME = ''
TRUST_REMOTE_CODE = True
MAX_TOKENS = 2000
TEMPERATURE = 0.7
BACKEND = "transformers"

# Logging settings
LOG_LEVEL = 'INFO'
LOG_FILE = os.path.join(LOGS_OUTPUT_DIR, 'pipeline.log')

# Ensure output directories exist
os.makedirs(FIXES_OUTPUT_DIR, exist_ok=True)
os.makedirs(LOGS_OUTPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
