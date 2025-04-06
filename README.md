# Automated Documentation Generator


## Overview


This tool automates the generation of documentation for Python codebases, including updating module listings, creating folder structures, and generating detailed docstrings. It leverages Ollama to produce comprehensive READMEs with entire LLM responses or specific extracted content.


## Features

- **Module Management**: Automatically updates a `modules.json` file listing all Python files in the project.
- **Folder Structure Generation**: Outputs a text file representing the directory structure of the codebase, excluding or including test directories based on user preference.
- **Docstring Generation**: Offers both basic and detailed docstrings for specified modules, utilizing the Abstract Syntax Tree (AST) to identify classes and functions.
- **README Creation**: Generates README files using Ollama, with options to include/exclude tests and use entire LLM responses or specific sections.

## Usage

### Command Line Arguments

- `-c`: Update `modules.json` and generate folder structure.
- `-a`: Collect codebase excluding test directories.
- `-at`: Include test directories when collecting the codebase.
- `-r`: Generate README using `modules.json`.
- `-ra`: Generate README excluding tests.
- `-rat`: Generate README including tests.
- `-re`: Use entire LLM response for README generation.
- `-d`: Generate basic docstrings.
- `-dd`: Generate detailed docstrings.

### Example Commands

1. **Update Module List and Folder Structure**

   ```bash
   python codecollect.py -c
   ```

2. **Generate Basic Docstrings**

   ```bash
   python codecollect.py -d
   ```

3. **Generate Detailed Docstrings**

   ```bash
   python codecollect.py -dd
   ```

4. **Create README with Entire LLM Response**

   ```bash
   python codecollect.py -re
   ```

## Structure

### Main Components

- **Module Management**: Uses `list_python_files` and `save_modules` to track Python files.
- **Folder Structure Generation**: Utilizes `generate_folder_structure` to create a representation of the directory layout.
- **Docstring Generation**: Employs `update_code` with AST parsing for inserting docstrings into code.
- **README Creation**: Leverages Ollama through `ollama_generate` to produce README content, appending folder structure.

### Configuration

- **Root Directory**: Set via `get_root_dir`.
- **Results Directory**: Configured using `get_results_dir`.

## Technical Details

- **Dependencies**: Requires Python 3.8+ and the `argparse`, `ast`, `os`, `json` libraries.
- **PEP 8 Compliance**: Ensures code adheres to PEP 8 standards, including max line length of 79 characters and single quotes for strings.

## Contributions

Feel free to contribute by improving functionality or enhancing documentation. Submit pull requests with clear descriptions of changes made.



# this README was also generated by codecollect
