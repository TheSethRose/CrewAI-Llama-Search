import os
from pathlib import Path
from typing import List, Set

# Additional files to ignore (not in .gitignore)
ADDITIONAL_IGNORES = {
    'generate.py'  # Utility files
}

# Core files that should always be included
CORE_FILES = {
    'main.py',
    'agents.py',
    'tools/tools.py',
    'src/config.py',
    'requirements.txt',
    '.env.example'
}

# File extensions that should be treated as text files
TEXT_EXTENSIONS = {
    '.py', '.md', '.txt', '.json', '.yaml', '.yml',
    '.ini', '.cfg', '.conf', '.env', '.sh', '.bash',
    '.css', '.html', '.js', '.ts', '.jsx', '.tsx'
}

def parse_gitignore() -> Set[str]:
    """Parse .gitignore file into a set of patterns."""
    patterns = set()
    try:
        with open('.gitignore', 'r') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if line and not line.startswith('#'):
                    # Remove leading and trailing slashes
                    pattern = line.strip('/')
                    patterns.add(pattern)
    except FileNotFoundError:
        pass

    # Add additional ignores
    patterns.update(ADDITIONAL_IGNORES)
    return patterns

def should_ignore(path: str, ignore_patterns: Set[str]) -> bool:
    """Check if path matches any gitignore pattern."""
    path = path.replace('\\', '/')  # Normalize path separators

    # Always include core files
    if path in CORE_FILES:
        return False

    # Check against all ignore patterns
    for pattern in ignore_patterns:
        # Handle directory patterns (ending with /)
        if pattern.endswith('/'):
            if path.startswith(pattern) or f"/{pattern}" in path:
                return True
        # Handle file patterns
        elif pattern in path:
            return True

    return False

def is_text_file(file_path: str) -> bool:
    """Check if a file is a text file based on its extension."""
    return Path(file_path).suffix.lower() in TEXT_EXTENSIONS

def read_file_content(file_path: str) -> str:
    """Read and return file content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def get_folder_structure(ignore_patterns: Set[str]) -> str:
    """Generate a tree-like folder structure."""
    structure = ["# Project Structure\n```"]
    prefix_map = {True: "├── ", False: "└── "}

    def add_to_structure(path: str, prefix: str = ""):
        entries = sorted(os.scandir(path), key=lambda e: (not e.is_dir(), e.name))
        filtered_entries = [e for e in entries if not should_ignore(e.path, ignore_patterns)]

        # Ensure .env.example is included in root
        if path == "." and os.path.exists(".env.example"):
            filtered_entries = sorted(filtered_entries + [Path(".env.example")], key=lambda e: (not e.is_dir() if isinstance(e, os.DirEntry) else True, e.name if isinstance(e, os.DirEntry) else str(e)))

        for idx, entry in enumerate(filtered_entries):
            is_last = (idx == len(filtered_entries) - 1)
            name = entry.name if isinstance(entry, os.DirEntry) else str(entry)
            structure.append(f"{prefix}{prefix_map[not is_last]}{name}")
            if isinstance(entry, os.DirEntry) and entry.is_dir():
                new_prefix = prefix + ("│   " if not is_last else "    ")
                add_to_structure(entry.path, new_prefix)

    add_to_structure(".")
    structure.append("```\n")
    return "\n".join(structure)

def add_line_numbers(content: str) -> str:
    """Add line numbers to content."""
    lines = content.splitlines()
    max_line_num = len(str(len(lines)))
    numbered_lines = []
    for i, line in enumerate(lines, 1):
        line_num = str(i).rjust(max_line_num)
        numbered_lines.append(f"{line_num} | {line}")
    return "\n".join(numbered_lines)

def generate_markdown() -> None:
    """Generate markdown file showing codebase structure with file contents."""
    ignore_patterns = parse_gitignore()

    # Start with the header
    markdown = "# CrewAI Project Codebase\n\n"

    # Check for .env and add note if present
    if os.path.exists('.env'):
        markdown += "> Note: This project uses a `.env` file for configuration (not shown for privacy). "
        markdown += "See `.env.example` for the required structure and setup instructions.\n\n"

    # Add folder structure
    markdown += get_folder_structure(ignore_patterns)
    markdown += "\n"

    # Walk through the directory
    for root, dirs, files in os.walk('.'):
        # Remove ignored directories
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), ignore_patterns)]

        # Process files
        for file in sorted(files):
            file_path = os.path.join(root, file)
            # Special handling for .env.example
            if file == '.env.example' or (not should_ignore(file_path, ignore_patterns) and is_text_file(file_path)):
                # Skip empty files
                if os.path.getsize(file_path) == 0:
                    continue

                # Get relative path
                rel_path = os.path.relpath(file_path, '.')

                # Add file header
                markdown += f"## {rel_path}\n\n"

                # Add file content in code block with line numbers
                content = read_file_content(file_path)
                file_ext = os.path.splitext(file)[1][1:]  # Get extension without dot
                markdown += f"```{file_ext}\n{add_line_numbers(content)}\n```\n\n"

    # Write the markdown file
    with open('project.md', 'w', encoding='utf-8') as f:
        f.write(markdown)

if __name__ == "__main__":
    generate_markdown()
