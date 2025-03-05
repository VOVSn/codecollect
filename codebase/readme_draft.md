# Python Script Guide

This document provides an overview of how to use the Python script designed for managing and documenting codebases. It explains various functionalities available through command-line arguments, including updating module configurations, generating documentation, and collecting codebases.

## Setup

Ensure you have a suitable Python environment set up with necessary dependencies installed. The script utilizes `argparse` for parsing command-line arguments and requires access to the file system for reading and writing files.

## Script Overview

The main script consists of several functions that interact with each other:

1. **File Management**: Functions like `list_python_files`, `save_modules`, and `load_modules` handle operations related to discovering Python files, saving module information, and loading this data.
   
2. **Documentation Generation**:
   - `generate_docstrings`: Generates basic or detailed docstrings for specified modules using the LLM model.
   - `update_code`: Updates source code with new docstrings and saves changes.

3. **README Creation**:
   - `generate_readme`: Creates a README file by sending the collected codebase to an LLM, extracting relevant documentation sections, and appending folder structure information.

4. **Code Collection**:
   - `collect_codebase`: Collects Python files into a single text document for processing.

5. **Folder Structure**: Utilizes functions like `generate_folder_structure` to create a representation of the directory layout.

## Command-Line Arguments

The script supports various command-line arguments that allow users to perform different tasks:

- `-c`: Update `modules.json` and generate folder structure.
- `-a`: Collect codebase, excluding test files.
- `-at`: Include test files when collecting the codebase.
- `-r`: Generate README using `modules.json`.
- `-ra`: Generate README while excluding tests.
- `-rat`: Generate README including tests.
- `-re`: Generate README with entire LLM response.
- `-d`: Generate basic docstrings for modules.
- `-dd`: Generate detailed docstrings for modules.

## Usage

To use the script, navigate to its directory in your terminal and execute it with desired arguments. For example:

```bash
python script_name.py -c   # Updates module configurations and generates folder structure.
python script_name.py -d   # Generates basic docstrings for all modules.
```

### Example Scenarios

1. **Updating Module Configurations**:
   
   Run the script with `-c` to update `modules.json`, reflecting current Python files in your project, excluding test directories unless `-at` is specified.

2. **Generating Docstrings**:

   Use `-d` for basic docstrings or `-dd` for detailed ones. Ensure that `modules.json` is up-to-date before running these options to apply changes to all relevant modules.

3. **Creating a README**:

   With `-r`, the script will generate a comprehensive README from `modules.json`. Add tests with `-rat` if needed, and use `-re` for full LLM responses in your documentation.

## Notes

- The script follows PEP 8 guidelines with a maximum line length of 79 characters.
- Ensure all paths (e.g., `results_dir`, `codebase_txt`) are correctly set within the script environment before execution.
- Handle exceptions gracefully, and review console output for any errors or warnings during operations.

This guide aims to provide clarity on utilizing the script's features effectively. For additional modifications or extensions, consider reviewing the source code for more in-depth understanding and customization opportunities.

## Folder Structure:
```
codecollect/
├── README.md
├── requirements.txt
├── setup.cfg
├── src
│   ├── codtest.py
│   └── main.py
```