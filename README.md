# RSS Feed Reader

![Pylint + PyTest](https://github.com/3nterz/rss-feed-reader/actions/workflows/pylint.yml/badge.svg)

RSS feed reader in terminal (Open source).

See [RSS feed reader in terminal](https://www.codementor.io/projects/tool/rss-feed-reader-in-terminal-atx32jp82q) for further information.

# Assumed Prerequisites

- Windows 10 Home Version 20H2
- Python 3.9.4 (64-bit)
- Visual Studio Code 1.60.1

# Project Set Up

1. Get the source code:

```powershell
git clone git@github.com:3nterz/rss-feed-reader.git
```

2. Go to the project folder in Windows CLI / Terminal, run the following commands:

```powershell
cd rss-feed-reader
python -m venv .venv
& ./.venv/Scripts/Activate.ps1
```

3. Run Visual Studio Code:

```powershell
code .
```

4. Set up Visual Studio Code Python Interpreter
- CTRL-SHIFT-P
- Type "Select interpreter" 
- Choose 'Enter interpreter path', click 'Find...'
- Browse to the '.venv\Scripts' folder
- Select the Python executable

5. Set up Visual Studio Code Python Unit Testing
- CTRL-SHIFT-P
- Type "Configure Tests"
- Choose 'unittest' Python test framework
- Choose '.' Root directory as the folder containing the tests
- Choose *_test.py - Python Files ending with '_test'

6. Set up Python library dependencies
- Specify libraries to be installed in the requirements.txt file
- Run command to install requirements 

```powershell
pip install -r requirements.txt
```

7. Run unit tests and check code coverage

```powershell
coverage run -m unittest app_test feedloaders_test
coverage report
```

8. Run pylint

```powershell
pylint (Get-ChildItem -path $FolderPath | Where-Object { $_.Extension -eq ".py"} | Foreach{ $_.Name })
```

9. Run the program

```powershell
python app.py --url url1 --url url2
```
