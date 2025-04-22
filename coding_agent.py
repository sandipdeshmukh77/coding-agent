import json
import os
from dotenv import load_dotenv
from openai import OpenAI
import platform

load_dotenv()
client = OpenAI(
    api_key=os.getenv('API_KEY_GEMINI'),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Tool functions


def detect_os(system=None):
  print(f"⛏️ Tool called : : detect_os : None")
  return platform.system()
   

def run_command(command):
    print(f"⛏️ Tool called : : run_command : {command}")
    try:
        return os.system(command)
    except Exception as e:
        return f"Error: {str(e)}"

def create_file(data):
    print(f"⛏️ Tool called : : create_file : {data}")
    # Handle both string and dict inputs

    file_name = data.get("file_name")
    content = data.get("content")

    # Validate inputs
    if not file_name or not content:
        return "Error: file_name and content are required"

    # Ensure string encoding
    try:
        if isinstance(content, str):
            content = content.encode('utf-8').decode('utf-8')
        if isinstance(file_name, str):
            file_name = file_name.encode('utf-8').decode('utf-8')
        
        # Write file
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"File {file_name} created successfully"
    except Exception as e:
        return f"Error creating file: {str(e)}"
    

def read_file(file_name):
    print(f"⛏️ Tool called : : read_file : {file_name}")
    try:
        with open(file_name, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error: {str(e)}"
    
def list_files(directory="."):
    print(f"⛏️ Tool called : : list_files : {directory}")
    try:
        files = os.listdir(directory)
        return f"Files in {directory}:\n" + "\n".join(files)
    except Exception as e:
        return f"Error: {str(e)}"

def delete_file(file_name):
    print(f"⛏️ Tool called : : delete_file : {file_name}")
    try:
        os.remove(file_name)
        return f"{file_name} deleted successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def git_command(command):
    print(f"⛏️ Tool called : : git_command : {command}")
    try:
        output = os.popen(f"git {command}").read()
        return output.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def get_current_directory(directory=None):
    # No input required for this function
    print(f"⛏️ Tool called : : get_current_directory : None")
    try:
        current_directory = os.getcwd()
        return f"Current directory: {current_directory}"
    except Exception as e:
        return f"Error: {str(e)}"
    
def make_directory(directory):
    print(f"⛏️ Tool called : : make_directory : {directory}")
    try:
        os.makedirs(directory, exist_ok=True)
        return f"Directory {directory} created successfully."
    except Exception as e:
        return f"Error: {str(e)}"


# Tool registry
available_tools = {
    "run_command": {
        "fn": run_command,
        "description": "Executes a shell command and returns output"
    },
    "create_file": {
        "fn":create_file,
        "description": "Creates and update a file with specified content"
    },
    "read_file": {
        "fn":read_file,
        "description": "Reads and returns the content of a file"
    },
        "list_files": {
        "fn": list_files,
        "description": "Lists all files in a specified directory"
    },
    "delete_file": {
        "fn":delete_file,
        "description": "Deletes the specified file"
    },
    "git_command": {
        "fn": git_command,
        "description": "Executes a git command like init, commit, etc."
    },
    "get_current_directory": {
        "fn": get_current_directory,
        "description": "Gets the current working directory"
    },
    "detect_os": {
        "fn": detect_os,
        "description": "Detects the operating system"
    },
    "make_directory": {
        "fn": make_directory,
        "description": "Creates a new directory"
    }
}

# System prompt
system_prompt = """
You are a helpful AI assistant specialized in writing code for fullstack application.
You operate in a loop of start â†’ plan â†’ action â†’ observe â†’ output.
For the given user query, reason step-by-step and use the available tools as needed.

Rules:
- Always respond with one JSON object per step.
- Wait for the observation after an action before proceeding.
- Carefully analyze the user request and think step-by-step.
- Use the available tools responsibly to complete the task.
- Validate inputs before executing commands.
- Check for errors in command outputs.
- Handle paths and directories safely.
- Keep security in mind when executing shell commands.
- Don't execute unsafe or malicious commands.
- Follow system-specific command syntax (Windows/Unix).
- Clean up temporary files when done.
- Maintain error handling for all operations.
- while executing commands if there is interaction needed like (y/n) then assume y or use default option.
- if target directory is already exists then delete it and create new one.

- For React app creation:
  - use command  that does not require user interaction like `npm create vite@latest my-react-app -- --template react`
  - After creating the app, install dependencies and suggest how to run it
  - Typical flow for React app: create app â†’ cd into directory â†’ npm install â†’ suggest npm run dev


Available Tools:
- run_command(command): Executes shell commands.
- create_file({file_name, content}): Creates and update a file with content.
- read_file(file_name): Reads content of a file.
- list_files(directory): Lists files in a directory.
- delete_file(file_name): Deletes a file.
- git_command(command): Executes Git commands.
- get_current_directory(): Gets the current working directory no input required.
- detect_os(): Detects the operating system.no input required`
- make_directory(directory): Creates a new directory.


Output JSON Format:
{
    "step": "plan" | "action" | "observe" | "output",
    "content": "string",
    "function": "name of function (only for action step)",
    "input": "input for the function (only for action step)"
}

Example : initiate a git repo in current directory
{ "step": "plan", "content": "I need to initialize a Git repo and list the files in the directory." }
{ "step": "action", "function": "git_command", "input":"init"}
{ "step": "observe", "content": "Initialized empty Git repository..." }
{ "step": "action", "function": "list_files", "input":"directory"}
{ "step": "observe", "content": "Files in .:\n.git\n..." }
{ "step": "output", "content": "Git repo initialized and here are the files in the directory." }

Example  : create react project with vite
{ "step": "plan", "content": "user wants to create react app using vite"}
{ "step": "action", "function": "run_command", "input": "npm create vite@latest my-react-app --template react" }
{ "step": "observe", "content": "Vite project created successfully" }
{"step": "action", "function": "run_command", "input": "cd my-react-app && npm install"}
{"step": "observe", "content": "Dependencies installed"}
{"step": "output", "content": "React application created successfully. You can start it by running 'cd my-react-app && npm run dev'"}


Example  : create navbar component in currect react project
{ "step": "plan", "content": "I need to create a Navbar component in the current React project." }
{ "step": "action", "function": "create_file", "input": "src/components/Navbar.js , <Navbar />" } }
{ "step": "observe", "content": "Navbar component created successfully." }
{ "step": "output", "content": "Navbar component created successfully." }

Example : Run npm start in background
{ "step": "plan", "content": "I'll run npm start in the background" }
{ "step": "action", "function": "run_command", "input": "start /B npm start" }
{ "step": "observe", "content": "Command executed" }
{ "step": "output", "content": "npm start is running in the background" }

Example : Run python script in background
{ "step": "plan", "content": "I'll run the Python script in background" }
{ "step": "action", "function": "run_command", "input": "start /B python test.py" }
{ "step": "observe", "content": "Command executed" }
{ "step": "output", "content": "Python script is running in background" }

Example : Install npm dependencies
{ "step": "plan", "content": "I'll install npm dependencies in background" }
{ "step": "action", "function": "run_command", "input":"start /B npm install" }
{ "step": "observe", "content": "Installation started" }
{ "step": "output", "content": "npm install is running in background" }
"""

# Message loop
messages = [
    { "role": "system", "content": system_prompt }
]

while True:
    user_query = input("You -: ")
    messages.append({ "role": "user", "content": user_query })

    while True:
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            response_format={"type": "json_object"},
            messages=messages
        )

        parsed_output = json.loads(response.choices[0].message.content)
        messages.append({ "role": "assistant", "content": json.dumps(parsed_output) })

        step = parsed_output.get("step")

        if step == "plan":
            # print(f"system -: {parsed_output.get('content')}")
            continue

        if step == "action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")
            if isinstance(tool_input, str):
                try:
                    tool_input = json.loads(tool_input)  # ensure dictionary
                except:
                    pass
            if tool_name in available_tools:
                result = available_tools[tool_name]["fn"](tool_input)
                messages.append({
                    "role": "assistant",
                    "content": json.dumps({ "step": "observe", "content": result })
                })
                continue

        if step == "output":
            print(f"system -: {parsed_output.get('content')}")
            break
