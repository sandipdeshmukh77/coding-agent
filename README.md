# Coding Agent

## Description

The Coding Agent is a Python-based application that leverages the Gemini API to provide a helpful AI assistant specialized in writing code for full-stack applications. It operates in a loop of planning, action, observation, and output. The agent has access to a set of tools that allow it to interact with the file system, execute shell commands, and perform Git operations.

## Features

*   **File System Operations:** Create, read, list, and delete files.
*   **Shell Command Execution:** Execute arbitrary shell commands.
*   **Git Operations:** Initialize, commit, and perform other Git commands.
*   **Environment Variable Support:** Uses `.env` files for configuration.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```

3.  **Activate the virtual environment:**
    *   **Windows:**
        ```bash
        .venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        source .venv/bin/activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirement.txt
    ```

5.  **Configure environment variables:**
    *   Create a `.env` file in the project root directory.
    *   Add your OpenAI API key to the `.env` file:
        ```
        API_KEY_GEMINI=<your_api_key>
        ```

## Usage

1.  **Run the agent:**
    ```bash
    python coding_agent.py
    ```

2.  **Interact with the agent:**
    *   The agent will prompt you with `> `.
    *   Enter your query, and the agent will respond with a plan, execute actions, and provide an output.

## Example

```
> Create a file named 'hello.txt' with the content 'Hello, world!'
```

## Contribution Guidelines

Contributions are welcome! To contribute:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Implement your changes.
4.  Submit a pull request.

## Batch File Usage

This project includes a batch file (`run_script.bat`) to automate common tasks. Here's how to use it:

1.  **Locate the Batch File:** Find the `run_script.bat` file in the project directory.
2.  **Open Command Prompt:** Open the Command Prompt (or Terminal on macOS/Linux).
3.  **Navigate to the Project Directory:** Use the `cd` command to navigate to the directory containing the batch file.
    ```bash
    cd path/to/your/project
    ```
4.  **Execute the Batch File:** Run the batch file by typing its name and pressing Enter.
    ```bash
    run_script.bat
    ```
5.  **Follow On-Screen Instructions:** The batch file might prompt you for input or display messages as it executes.

## Advantages of Using Batch Files

*   **Automation:** Batch files automate repetitive tasks, saving time and effort.
*   **Efficiency:** They execute a series of commands sequentially, ensuring consistency.
*   **Simplicity:** Batch files are easy to create and modify, even for users with limited programming experience.
*   **Customization:** You can tailor batch files to specific needs and workflows.

## Example `run_script.bat` Content
```batch
@echo off
echo Running a sample task...
echo Creating a directory named 'output'...
mkdir output
echo Done.
pause
```

## Notes

*   Ensure you have the necessary permissions to execute batch files.
*   Modify the batch file to suit your specific requirements.
