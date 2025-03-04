# CodeCollect

## Project Overview

CodeCollect is a Python utility designed for analyzing Python codebases containing multiple modules. Its primary function is to generate a detailed `README.md` file following best Git practices. The tool automates several tasks including collecting module files, updating configuration files, and integrating with the Ollama API to create comprehensive documentation.

## Installation

To set up CodeCollect on your system, follow these steps:

1. **Prerequisites:**
   - Ensure Python 3.x is installed.
   - Install necessary dependencies:
     ```bash
     pip install requests
     ```

2. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/codecollect.git
   cd codecollect
   ```

3. **Configuration (Optional):**
   - Create a `modules.json` file in the root directory if it doesn't exist.
   - Customize paths and settings as needed within the script.

## Tech Stack

- **Python:** Core programming language used for scripting.
- **Requests Library:** Used for interacting with the Ollama API.
- **Argparse Library:** For command-line argument parsing.
- **OS Module:** To interact with the file system.

## Usage

CodeCollect provides a variety of command-line options to control its behavior:

```bash
python codecollect.py [options]
```

### Available Options

- `-c`: Update `modules.json` (excludes tests).
- `-a`: Collect codebase excluding tests.
- `-at`: Include tests when collecting the codebase.
- `-r`: Generate README using `modules.json`.
- `-ra`: Generate README excluding tests.
- `-rat`: Generate README including tests.
- `-re`: Generate README with the entire LLM response.

### Example Commands

1. **Update Modules:**
   ```bash
   python codecollect.py -c
   ```

2. **Collect Codebase Excluding Tests:**
   ```bash
   python codecollect.py -a
   ```

3. **Generate README (Excluding Tests):**
   ```bash
   python codecollect.py -ra
   ```

4. **Generate Full LLM Response in README:**
   ```bash
   python codecollect.py -re
   ```

## Functionality

- **Module Collection:** Gathers all Python files, excluding tests by default.
- **Configuration Management:** Updates and maintains `modules.json`.
- **Documentation Generation:** Creates a detailed README using Ollama API integration.

### Additional Capabilities

- Supports inclusion of test modules if specified.
- Generates both draft and full README versions based on user preferences.

## Git Best Practices

To maintain the quality and consistency of the CodeCollect project, adhere to these guidelines:

- **Branching Strategy:**
  - Use feature branches for new developments (`feature/<name>`).
  - Use a `main` branch for stable releases.
  
- **Commit Messages:**
  - Write clear and concise commit messages.
  - Follow the format: `<type>: <description>`.
  
- **Pull Requests:**
  - Ensure code reviews are conducted before merging.
  - Resolve conflicts and run tests before submitting.

## Contributing

Contributions to CodeCollect are welcome! Here’s how you can contribute:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bug fix.
3. Implement your changes, ensuring compliance with PEP 8 standards.
4. Submit a pull request with a clear description of your changes.

## License

CodeCollect is licensed under the MIT License. See [LICENSE](https://github.com/yourusername/codecollect/blob/main/LICENSE) for more information.