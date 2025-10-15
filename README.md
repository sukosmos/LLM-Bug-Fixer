# Bug Fixing Pipeline

## Overview
The Bug Fixing Pipeline is a Python project designed to automate the process of identifying and fixing bugs in code files using a combination of fault localization and code generation techniques powered by a language model (LLM). This project aims to streamline the debugging process, making it more efficient and effective.

## Project Structure
```
bug-fixing-pipeline/
├── src/
│   ├── __init__.py          # Initializes the src package
│   ├── find_file.py         # Scans for buggy files
│   ├── find_FL.py           # Localizes faults in buggy code
│   ├── fix_code.py          # Generates code fixes
│   └── test_fix.py          # Runs test cases
├── mcp_client.py            # Main client to orchestrate the pipeline
├── llm_client.py            # Handles interaction with the LLM
├── requirements.txt         # Lists project dependencies
├── config.py                # Configuration settings
└── README.md                # Project documentation
```

## Installation
To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd bug-fixing-pipeline
pip install -r requirements.txt
```

## Usage
1. **Finding Buggy Files**: The pipeline starts by scanning a specified directory for files that contain known bug patterns. This is done using the `find_buggy_files` function in `src/find_file.py`.

2. **Fault Localization**: Once buggy files are identified, the `FaultLocalizer` class in `src/find_FL.py` is used to analyze the code and pinpoint potential fault locations.

3. **Generating Fixes**: The identified faults are then passed to the `CodeFixer` class in `src/fix_code.py`, which generates code fixes using the LLM.

4. **Running Tests**: Finally, the `run_tests` function in `src/test_fix.py` executes the relevant test cases to verify that the fixes work as intended.

## Configuration
Configuration settings such as input and output paths, model parameters, and logging settings can be adjusted in `config.py`.

## Dependencies
The project relies on several libraries for LLM interaction, file handling, and testing. These are listed in `requirements.txt`.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.