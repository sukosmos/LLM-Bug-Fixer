# LLM Bug Fixer

Automated bug fixing pipeline using Large Language Models (LLM).

## Overview

This pipeline automatically:
1. **Localizes faults** in Java code using LLM
2. **Generates fixes** for identified bugs
3. **Validates fixes** through compilation and testing

## Features

- 🔍 **Fault Localization**: LLM analyzes code to identify bugs
- 🔧 **Automated Fixing**: Generates corrected code
- ✅ **Test Validation**: Compiles and runs tests on fixes
- 📊 **Token Tracking**: Monitors LLM token usage
- 📝 **Detailed Logging**: Saves all results in JSON format

## Project Structure

```
llm_bug_fixer/
├── main.py                 # Main pipeline execution
├── config.py              # Configuration settings
├── llm_client.py          # vLLM client wrapper
├── src/
│   ├── file_utils.py      # File I/O utilities
│   ├── find_FL.py         # Fault localization
│   ├── fix_code.py        # Code fixing
│   └── test_fix.py        # Test execution
├── data/
│   ├── target/            # Buggy Java files
│   └── test/              # JUnit test files
└── output/
    ├── fixes/             # Fixed code + JSON results
    └── logs/              # Execution logs
```

## Installation

```bash
# Create virtual environment
python -m venv vllm_env
source vllm_env/bin/activate

# Install dependencies
pip install vllm torch transformers
```

## Usage

```bash
# Place buggy Java files in data/target/
# Place corresponding test files in data/test/

# Run the pipeline
python main.py
```

## Configuration

Edit `config.py` to customize:
- Model name (default: EXAONE-3.0-7.8B-Instruct)
- Temperature, max tokens
- Input/output directories

## Output

Each processed file produces:
- `output/fixes/{filename}.java` - Fixed code
- `output/fixes/{filename}.java.json` - Complete results:
  - Fault localization findings
  - Token usage (FL + Fix)
  - Test results

## Example Output JSON

```json
{
  "file": "Calculator.java",
  "fl": {
    "faults": ["Line 5: Method returns wrong value"],
    "token_usage": {"prompt_tokens": 150, "completion_tokens": 80}
  },
  "fix": {
    "fixed_file": "output/fixes/Calculator.java",
    "token_usage": {"prompt_tokens": 200, "completion_tokens": 150}
  },
  "test": {
    "compiled": true,
    "passed": 4,
    "failed": 1
  }
}
