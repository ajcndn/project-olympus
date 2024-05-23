# Project Olympus

## Overview
This repository hosts the updated Olympus project.

## Features
- **Hierarchical Task Management:** Leverage the power of structured task execution to maintain a clean and scalable codebase.
- **Asynchronous Tasks:** Improve performance with non-blocking operations, allowing tasks to run concurrently.
- **Callbacks:** Ensure that each task can trigger subsequent actions upon completion, enabling a reactive task flow.
- **Expected Outputs:** Define the anticipated results for each task, streamlining debugging and ensuring quality control.

## Installation
To get started, clone the repository and install the necessary dependencies.

```
git clone https://github.com/your-github-username/project-olympus.git
cd Project-Olympus
Run 'poetry install --no-root' to install the required packages.

```

## Usage
Rename the .env.example file to .env and fill in the required environment variables for OPENAI_API_KEY & SERPER_API_KEY
To launch the Olympus_streamlit application run the following command: streamlit run main.py
To launch the Olympus_panel application run the following command: panel serve olympus_panel.py
Launch the panel URL from console (http://localhost:5006/olympus)

```

## Structure
main.py: The entry point script that initializes the agents and tasks, and forms the AI crew.

agents.py: Defines various agents like the editor, news fetcher, news analyzer, and newsletter compiler.

tasks.py: Contains the task definitions that are used by the agents to perform specific operations.

file_io.py: Manages file input/output operations, crucial for handling the async flow of data.




#
