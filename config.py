# config.py

import os

# Configuration settings for the bug-fixing pipeline

# Input and output directories
INPUT_DIR = os.path.join('data', 'target')
TEST_DIR = os.path.join('data', 'test')
OUTPUT_DIR = 'output'
FIXES_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'fixes')
LOGS_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'logs')

# Model parameters - vLLM 로컬 인스턴스
LLM_MODEL_NAME = 'LGAI-EXAONE/EXAONE-3.0-7.8B-Instruct'
TRUST_REMOTE_CODE = True
MAX_TOKENS = 2000
TEMPERATURE = 0.7

# Logging settings
LOG_LEVEL = 'INFO'
LOG_FILE = os.path.join(LOGS_OUTPUT_DIR, 'pipeline.log')

# Ensure output directories exist
os.makedirs(FIXES_OUTPUT_DIR, exist_ok=True)
os.makedirs(LOGS_OUTPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)