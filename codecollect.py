import ast
import os
import json
import argparse


# Try importing requests and httpx at the top level
try:
    import requests
    HTTP_LIB = 'requests'
except ImportError:
    requests = None
    HTTP_LIB = None

try:
    import httpx
    HTTP_LIB = 'httpx'
except ImportError:
    httpx = None
    if not HTTP_LIB:  # If requests also failed
        HTTP_LIB = None

# Constants
DEBUG = True  # Toggle manually; True saves to *_doc.py, False replaces with backup
LANGUAGE = "russian"  # Edit to "russian", "spanish", etc.
DOCSTRING_OVERRIDE = "skip"  # "skip" (only if missing), "size" (longest), "llm" (always Ollama)
IGNORED_FOLDERS = ['env', '.git', 'codebase']
DOCSTRING_PROMPT = (
    "Analyze this Python code and generate docstrings in {LANGUAGE}. "
    "Return ONLY a JSON object with keys as element names (e.g., 'module', 'class MyClass', 'def myfunc') "
    "and values as docstrings. Do NOT include any text, explanations, or examples outside the JSON. "
    "Response format: {{'module': 'docstring', 'MyClass': 'docstring', 'myfunc': 'docstring'}}\n"
    "Code:\n"
    "```python\n{code}\n```\n"
)
DETAILED_DOCSTRING_PROMPT = (
    f"Generate detailed docstrings in {{LANGUAGE}} for this Python module, "
    "including arguments, return values. "
    "Return a JSON object with keys as element names (e.g., 'module', 'class MyClass', 'def myfunc') "
    "and values as docstrings:\n"
    "```python\n{code}\n```\n"
    "Response format: {{'module': 'docstring', 'MyClass': 'docstring', 'myfunc': 'docstring'}}"
)
README_PROMPT = (
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
    "\"{codebase}\"\n"
    "Ensure every section is comprehensive and detailed. Encapsulate your response in triple ticks: "
    "```contents of readme.md```"
)
FOLDER_STRUCTURE_SECTION = (
    "\n\n## Folder Structure:\n"
    "```\n"
    "{folder_structure}\n"
    "```"
)
CODING_GUIDELINES = (
    '\n---\n'
    'Ensure compliance with:\n'
    '- Max line length: 79 characters\n'
    '- PEP 8 formatting\n'
    '- Single quotes for strings\n'
    '- Double blank lines between classes and functions\n'
    'Refactor if necessary.\n'
    '---\n'
)

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
        entries = sorted(os.listdir(path))
        lines = []
        for i, entry in enumerate(entries):
            entry_path = os.path.join(path, entry)
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
        outfile.write(CODING_GUIDELINES)

def ollama_generate(prompt, as_dict=False):
    if HTTP_LIB is None:
        raise ImportError("Neither 'requests' nor 'httpx' is installed. Please install one.")

    OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"
    payload = {"model": "phi4", "prompt": prompt, "stream": False}
    for attempt in range(3):
        try:
            if HTTP_LIB == 'requests' and requests:
                response = requests.post(OLLAMA_API_URL, json=payload, timeout=30)
            elif HTTP_LIB == 'httpx' and httpx:
                response = httpx.post(OLLAMA_API_URL, json=payload, timeout=30)
            response.raise_for_status()
            raw_text = response.text
            print(f"Raw API response: {raw_text}")
            result = response.json()
            raw_response = result.get("response", "")
            print(f"Extracted response: {raw_response}")
            if as_dict:
                try:
                    return json.loads(raw_response)
                except json.JSONDecodeError:
                    start_marker = '```json'
                    end_marker = '```'
                    if start_marker in raw_response and end_marker in raw_response:
                        start_idx = raw_response.index(start_marker) + len(start_marker)
                        end_idx = raw_response.rindex(end_marker)
                        json_str = raw_response[start_idx:end_idx].strip()
                        try:
                            return json.loads(json_str)
                        except json.JSONDecodeError:
                            print(f"Failed to parse JSON block: {json_str}")
                    print("No valid JSON found, returning empty dict")
                    return {}
            return raw_response
        except Exception as e:
            print(f"Ollama API error on attempt {attempt + 1}: {str(e)}")
            if attempt == 2:
                print("All attempts failed, returning default value")
                return {} if as_dict else ""
    return {} if as_dict else ""

def extract_elements(tree):
    elements = {}
    module_doc = ast.get_docstring(tree)
    if module_doc:
        elements["module"] = (0, module_doc)
    else:
        elements["module"] = (0, None)
    
    def get_parent_class(node, tree):
        for parent in ast.walk(tree):
            if isinstance(parent, ast.ClassDef) and node in parent.body:
                return parent.name
        return None
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            name = f"class {node.name}"
            doc = ast.get_docstring(node)
            pos = node.lineno - 1
            elements[name] = (pos, doc)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            parent_class = get_parent_class(node, tree)
            if parent_class:
                name = f"{parent_class}.{node.name}"
            else:
                name = f"def {node.name}"
            doc = ast.get_docstring(node)
            pos = node.lineno - 1
            elements[name] = (pos, doc)
    return elements

def update_code(code, elements, docstrings, detailed=False):
    lines = code.splitlines()
    for name, (pos, existing_doc) in sorted(elements.items(), key=lambda x: x[1][0], reverse=True):
        base_name = name.split('.')[-1] if '.' in name else name.replace("class ", "").replace("def ", "")
        key_options = [name, base_name, f"def {base_name}"]
        new_doc = next((docstrings.get(key, "").strip() for key in key_options if key in docstrings), "")
        if not new_doc:
            continue
        
        indent = ""
        if name == "module":
            indent = ""
        elif name.startswith("def "):  # Top-level function
            indent = "    "
        elif "." in name:  # Method in class
            indent = "        "
        elif name.startswith("class "):
            indent = "    "
        
        max_line_length = 79 - len(indent)
        doc_lines = [f'{indent}"""']
        for line in new_doc.splitlines():
            while len(line) > max_line_length:
                split_pos = line.rfind(" ", 0, max_line_length)
                if split_pos == -1:
                    split_pos = max_line_length
                doc_lines.append(f"{indent}{line[:split_pos]}")
                line = line[split_pos:].lstrip()
            doc_lines.append(f"{indent}{line}")
        doc_lines.append(f'{indent}"""')
        
        # Insertion position
        if name == "module":
            insert_pos = 0
        elif name.startswith("class "):
            insert_pos = pos + 1  # Right after class definition
        else:  # Functions and methods
            start_line = pos
            insert_pos = start_line
            paren_count = 0
            for i in range(start_line, len(lines)):
                line = lines[i]
                paren_count += line.count('(') - line.count(')')
                if paren_count == 0 and ')' in line:
                    insert_pos = i + 1
                    break
        
        if existing_doc:
            if DOCSTRING_OVERRIDE == "skip":
                continue
            elif DOCSTRING_OVERRIDE in ("size", "llm"):
                doc_start = insert_pos
                while doc_start < len(lines) and not lines[doc_start].strip().startswith('"""'):
                    doc_start += 1
                if doc_start < len(lines):
                    doc_end = doc_start
                    while doc_end < len(lines) and not lines[doc_end].strip().endswith('"""'):
                        doc_end += 1
                    if DOCSTRING_OVERRIDE == "size" and len(new_doc) <= len(existing_doc):
                        continue
                    lines[doc_start:doc_end + 1] = doc_lines
                else:
                    lines.insert(insert_pos, "\n".join(doc_lines))
        else:
            lines.insert(insert_pos, "\n".join(doc_lines))
    
    return "\n".join(lines) + "\n"

def save_file(module_path, new_code, module):
    """Save the updated code based on DEBUG setting."""
    if DEBUG:
        output_path = f"{module_path.rsplit('.', 1)[0]}_doc.py"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(new_code)
    else:
        backup_path = f"{module_path}.bak"
        if os.path.exists(module_path):
            os.rename(module_path, backup_path)
        with open(module_path, 'w', encoding='utf-8') as f:
            f.write(new_code)

def generate_docstrings(modules, detailed=False):
    root_dir = get_root_dir()
    for module in modules:
        module_path = os.path.join(root_dir, module)
        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                code = f.read()
            tree = ast.parse(code)
            elements = extract_elements(tree)
            
            prompt = (DETAILED_DOCSTRING_PROMPT if detailed else DOCSTRING_PROMPT).format(
                LANGUAGE=LANGUAGE, code=code
            )
            print(f"Prompt sent to Ollama:\n{prompt}")
            
            # Retry up to 3 times if async functions lack docstrings
            max_retries = 3
            for attempt in range(max_retries + 1):
                docstrings = ollama_generate(prompt, as_dict=True)
                print(f"Attempt {attempt + 1}: Docstrings received: {docstrings}")
                
                # Check if all async functions have docstrings
                async_missing = False
                for name in elements:
                    if "def " in name and "async" in code.splitlines()[elements[name][0]]:
                        if not docstrings.get(name.replace("def ", ""), ""):
                            async_missing = True
                            break
                
                if not async_missing or attempt == max_retries:
                    break
                print(f"Retrying for {module} due to missing async docstrings...")
            
            if not docstrings:
                print(f"module {module} skipped after {max_retries + 1} attempts, using fallback")
                docstrings = {"module": "Fallback module docstring"}
                for name in elements:
                    if name != "module":
                        docstrings[name.replace("class ", "").replace("def ", "")] = f"Fallback docstring for {name}"
            
            new_code = update_code(code, elements, docstrings, detailed)
            save_file(module_path, new_code, module)
            print(f"Docstrings for {module} ready")
        except Exception as e:
            print(f"Error processing {module}: {str(e)}")

def generate_readme(codebase_file, output_file, entire_response=False):
    """Send the codebase to Ollama and generate a README with folder structure appended."""
    results_dir = get_results_dir()
    os.makedirs(results_dir, exist_ok=True)
    with open(codebase_file, 'r', encoding='utf-8') as f:
        codebase = f.read()
    prompt = README_PROMPT.format(codebase=codebase)
    response = ollama_generate(prompt)
    
    if not isinstance(response, str):
        print(f"Warning: Expected string response from Ollama, got {type(response)}. Using empty content.")
        readme_content = ""
    elif entire_response:
        readme_content = response
    else:
        start_marker = '```'
        end_marker = '```'
        try:
            start_idx = response.index(start_marker) + len(start_marker)
            end_idx = response.rindex(end_marker)
            readme_content = response[start_idx:end_idx].strip()
        except ValueError:
            print("Warning: Could not extract README content between ``` markers. Using full response.")
            readme_content = response

    root_dir = get_root_dir()
    folder_structure_file = os.path.join(results_dir, "folder_structure.txt")
    generate_folder_structure(root_dir, "folder_structure.txt")
    with open(folder_structure_file, 'r', encoding='utf-8') as f:
        folder_structure = f.read()
    readme_content += FOLDER_STRUCTURE_SECTION.format(folder_structure=folder_structure)

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
    parser.add_argument("-d", action="store_true", help="Generate basic docstrings")
    parser.add_argument("-dd", action="store_true", help="Generate detailed docstrings")
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

    if args.d or args.dd:
        modules = load_modules(modules_file)
        generate_docstrings(modules, detailed=args.dd)
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