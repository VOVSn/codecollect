import os
import json
import argparse

# Check for requests or httpx availability
try:
    import requests
    HTTP_LIB = 'requests'
except ImportError:
    requests = None

try:
    import httpx
    HTTP_LIB = 'httpx'
except ImportError:
    httpx = None

if not (requests or httpx):
    raise ImportError("Neither 'requests' nor 'httpx' is installed.")

# List of folder names to ignore (case-insensitive)
IGNORED_FOLDERS = ['env', '.git', 'codebase']

def get_root_dir():
    """Get the root directory where codecollect.py is located."""
    return os.path.dirname(os.path.abspath(__file__))

def get_results_dir():
    """Get the results directory (codebase) relative to the root."""
    return os.path.join(get_root_dir(), "codebase")

def list_python_files(root_dir):
    """List all Python files, excluding codecollect.py and ignored folders."""
    py_files = []
    for root, _, files in os.walk(root_dir):
        # Check if any ignored folder name is in the path (case-insensitive)
        if any(ignored in root.lower() for ignored in IGNORED_FOLDERS):
            continue
        for file in files:
            if file.endswith(".py") and file != "codecollect.py" and file != "__init__.py":
                rel_path = os.path.relpath(os.path.join(root, file), root_dir).replace('\\', '/')
                py_files.append(rel_path)
    return py_files

def generate_folder_structure(root_dir, output_file):
    """Generate a folder structure tree and save it to a file, excluding ignored folders."""
    results_dir = get_results_dir()
    os.makedirs(results_dir, exist_ok=True)
    output_path = os.path.join(results_dir, output_file)
    
    def build_tree(path, prefix=""):
        """Recursively build the folder structure."""
        entries = sorted(os.listdir(path))
        lines = []
        for i, entry in enumerate(entries):
            entry_path = os.path.join(path, entry)
            # Skip ignored folders, hidden files, and codecollect.py
            if (any(ignored in entry.lower() for ignored in IGNORED_FOLDERS) or 
                entry.startswith('.') or entry == 'codecollect.py'):
                continue
            is_last = i == len(entries) - 1
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{entry}")
            if os.path.isdir(entry_path) and not any(ignored in entry.lower() for ignored in IGNORED_FOLDERS):
                extension = "    " if is_last else "│   "
                lines.extend(build_tree(entry_path, prefix + extension))
        return lines

    tree_lines = [os.path.basename(root_dir) + "/"] + build_tree(root_dir)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(tree_lines))

def load_modules(modules_file):
    """Load modules from modules.json, creating it if it doesn't exist."""
    os.makedirs(os.path.dirname(modules_file), exist_ok=True)
    if not os.path.exists(modules_file):
        with open(modules_file, 'w', encoding='utf-8') as f:
            json.dump({"modules": []}, f, indent=2, ensure_ascii=False)
    with open(modules_file, 'r', encoding='utf-8') as f:
        return json.load(f).get("modules", [])

def save_modules(modules_file, modules):
    """Save module list to modules.json, creating directory if needed."""
    os.makedirs(os.path.dirname(modules_file), exist_ok=True)
    with open(modules_file, 'w', encoding='utf-8') as f:
        json.dump({"modules": modules}, f, indent=2, ensure_ascii=False)

def collect_codebase(output_file, modules):
    """Collect specified modules into a single text file in the results directory."""
    root_dir = get_root_dir()
    results_dir = get_results_dir()
    os.makedirs(results_dir, exist_ok=True)
    output_path = os.path.join(results_dir, output_file)
    with open(output_path, 'w', encoding='utf-8') as outfile:
        for module in modules:
            module_path = os.path.join(root_dir, module)
            try:
                with open(module_path, 'r', encoding='utf-8') as infile:
                    contents = infile.read()
                outfile.write(f"{module}:\n\n```")
                outfile.write(f"\n{contents}\n" if contents.endswith('\n') else f"\n{contents}\n")
                outfile.write("```\n\n")
            except FileNotFoundError:
                outfile.write(f"{module}:\n\n```")
                outfile.write(f"\n# File not found: {module_path}\n")
                outfile.write("```\n\n")
        outfile.write(
            '\n---\n'
            'Ensure compliance with:\n'
            '- Max line length: 79 characters\n'
            '- PEP 8 formatting\n'
            '- Single quotes for strings\n'
            '- Double blank lines between classes and functions\n'
            'Refactor if necessary.\n'
            '---\n'
        )

def ollama_generate(prompt):
    """Generate a response using Ollama API with available HTTP library."""
    OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"
    payload = {"model": "phi4", "prompt": prompt, "stream": False}
    try:
        if HTTP_LIB == 'requests' and requests:
            response = requests.post(OLLAMA_API_URL, json=payload, timeout=30)
        elif HTTP_LIB == 'httpx' and httpx:
            response = httpx.post(OLLAMA_API_URL, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "")
    except Exception as e:
        print(f"Ollama API error: {str(e)}")
        return ""

def generate_readme(codebase_file, output_file, entire_response=False):
    """Send the codebase to Ollama and generate a README with folder structure appended."""
    results_dir = get_results_dir()
    os.makedirs(results_dir, exist_ok=True)
    with open(codebase_file, 'r', encoding='utf-8') as f:
        codebase = f.read()
    prompt = (
        "You are tasked with analyzing the user's Python codebase, which includes multiple modules. "
        "Your goal is to create a detailed `readme.md` file following best Git practices. "
        "Here’s what to include:\n"
        "- **Project Overview**: Describe the purpose and main functionality of the program.\n"
        "- **Installation**: Provide step-by-step instructions to set up the project, including dependencies.\n"
        "- **Tech Stack**: List all technologies, libraries, and tools used.\n"
        "- **Usage**: Explain how to run the program with detailed examples (e.g., command-line arguments).\n"
        "- **Functionality**: Detail all features and capabilities, inferring additional ones if possible.\n"
        "- **Git Best Practices**: Include guidelines for branching, committing, and contributing.\n"
        "- **Contributing**: Outline how others can contribute (e.g., pull requests, issues).\n"
        "- **License**: Suggest a suitable license (e.g., MIT) if not specified.\n"
        "Base your analysis on this codebase:\n"
        f"\"{codebase}\"\n"
        "Ensure every section is comprehensive and detailed. Encapsulate your response in triple ticks: "
        "```contents of readme.md```"
    )
    response = ollama_generate(prompt)
    
    if entire_response:
        readme_content = response
    else:
        start_marker = '```'
        end_marker = '```'
        try:
            start_idx = response.index(start_marker) + len(start_marker)
            end_idx = response.rindex(end_marker)
            readme_content = response[start_idx:end_idx].strip()
        except ValueError:
            readme_content = response

    # Append folder structure
    root_dir = get_root_dir()
    folder_structure_file = os.path.join(results_dir, "folder_structure.txt")
    generate_folder_structure(root_dir, "folder_structure.txt")
    with open(folder_structure_file, 'r', encoding='utf-8') as f:
        folder_structure = f.read()
    readme_content += (
        "\n\n## Folder Structure:\n"
        "```\n"
        f"{folder_structure}\n"
        "```"
    )

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", action="store_true", help="Update modules.json and generate folder structure")
    parser.add_argument("-a", action="store_true", help="Collect codebase excluding tests")
    parser.add_argument("-at", action="store_true", help="Include tests when collecting")
    parser.add_argument("-r", action="store_true", help="Generate README using modules.json")
    parser.add_argument("-ra", action="store_true", help="Generate README excluding tests")
    parser.add_argument("-rat", action="store_true", help="Generate README including tests")
    parser.add_argument("-re", action="store_true", help="Generate README with entire LLM response")
    args = parser.parse_args()

    root_dir = get_root_dir()
    results_dir = get_results_dir()
    modules_file = os.path.join(results_dir, "modules.json")
    codebase_txt = os.path.join(results_dir, "codebase.txt")
    readme_md = os.path.join(results_dir, "readme_draft.md")

    if args.c:
        modules = list_python_files(root_dir)
        if not args.at:
            modules = [m for m in modules if "test_" not in m]
        save_modules(modules_file, modules)
        generate_folder_structure(root_dir, "folder_structure.txt")
        print("Updated modules.json and generated folder_structure.txt.")
        return

    if args.a or args.ra or args.rat or args.re:
        modules = list_python_files(root_dir)
        if (args.a or args.ra) and not args.at:
            modules = [m for m in modules if "test_" not in m]
    else:
        modules = load_modules(modules_file)
        if not modules:
            modules = list_python_files(root_dir)
            modules = [m for m in modules if "test_" not in m]
            save_modules(modules_file, modules)

    collect_codebase(codebase_txt, modules)

    if args.r or args.ra or args.rat or args.re:
        generate_readme(codebase_txt, readme_md, entire_response=args.re)
        print("Generated README draft with folder structure.")

if __name__ == "__main__":
    main()