# RSS Feed Reader

RSS feed reader in terminal

# Assumed Prerequisites

- Windows 10 Home Version 20H2
- Python 3.9.4 (64-bit)
- Visual Studio Code 1.59.0

# Project Set Up

1. In Windows CLI / Terminal, run the following commands

- python -m venv .venv
- .\.venv\Scripts\activate.bat

2. Run Visual Studio Code and create or open files
- code app.py app_test.py .gitignore requirements.txt

3. Set up Visual Studio Code Python Interpreter
- CTRL-SHIFT-P
- Type "Select interpreter" 
- Choose 'Enter interpreter path', click 'Find...'
- Browse to the '.venv\Scripts' folder
- Select the Python executable

4. Set up Visual Studio Code Python Unit Testing
- CTRL-SHIFT-P
- Type "Configure Tests"
- Choose 'unittest' Python test framework
- Choose '.' Root directory as the folder containing the tests
- Choose *_test.py - Python Files ending with '_test'

5. Set up Python library dependencies
- Specify libraries to be installed in the requirements.txt file
- Run pip install -r requirements.txt

6. Run unit tests and code coverage
- coverage -m unittest app_test
- coverage report