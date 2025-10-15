# config.py

import os

# Configuration settings for the bug-fixing pipeline

# Input and output directories
INPUT_DIR = os.path.join('data', 'buggy_files')
OUTPUT_DIR = 'output'
FL_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'fl')
FIXES_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'fixes')
LOGS_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'logs')
TOKEN_USAGE_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'token_usage')
TEST_RESULTS_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'test_results')

# Model parameters
LLM_MODEL_NAME = 'vllm_model_name'  # Replace with the actual model name
LLM_API_KEY = 'your_api_key_here'    # Replace with your actual API key

# Logging settings
LOG_LEVEL = 'INFO'  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = os.path.join(LOGS_OUTPUT_DIR, 'pipeline.log')

# Other configurations can be added as needed