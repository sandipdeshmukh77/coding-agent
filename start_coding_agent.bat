@echo off
REM Activate the virtual environment and run coding_agent.py

pushd "ADD ABSOLUTE PATH TO YOUR PROJECT FOLDER WHERE coding_agent.py IS LOCATED"

if exist ".venv\Scripts\activate.bat" (
  call .venv\Scripts\activate.bat
  python coding_agent.py
) else (
  echo Error: Virtual environment not found. Please create it first.
  pause
)

popd
pause