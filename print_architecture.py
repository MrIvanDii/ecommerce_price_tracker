"""
print_architecture.py
Запускай из корня проекта: python print_architecture.py
Выводит дерево файлов + сохраняет в ARCHITECTURE.md
"""

import os
from pathlib import Path
from datetime import datetime

# --- Настройки ---
ROOT = Path(__file__).parent  # корень = папка где лежит скрипт
OUTPUT_FILE = ROOT / "ARCHITECTURE.md"

IGNORE_DIRS = {
    ".venv", "venv", "__pycache__", ".git", ".idea",
    ".pytest_cache", "node_modules", ".mypy_cache", "dist", "build",
}
IGNORE_FILES = {
    ".DS_Store", "*.pyc", "*.pyo", "*.pyd",
}
IGNORE_EXTENSIONS = {".pyc", ".pyo", ".pyd"}


def should_ignore(path: Path) -> bool:
    if path.name in IGNORE_DIRS:
        return True
    if path.suffix in IGNORE_EXTENSIONS:
        return True
    for pattern in IGNORE_FILES:
        if path.match(pattern):
            return True
    return False


def build_tree(directory: Path, prefix: str = "") -> list[str]:
    lines = []

    try:
        entries = sorted(directory.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    except PermissionError:
        return lines

    entries = [e for e in entries if not should_ignore(e)]

    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        connector = "└── " if is_last else "├── "
        extension = "    " if is_last else "│   "

        if entry.is_dir():
            lines.append(f"{prefix}{connector}{entry.name}/")
            lines.extend(build_tree(entry, prefix + extension))
        else:
            size = entry.stat().st_size
            size_str = f"  [{size:,} bytes]" if size > 0 else ""
            lines.append(f"{prefix}{connector}{entry.name}{size_str}")

    return lines


def main():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tree_lines = build_tree(ROOT)

    output_lines = [
        f"# Project Architecture",
        f"",
        f"Generated: {timestamp}",
        f"Root: `{ROOT}`",
        f"",
        f"```",
        f"{ROOT.name}/",
        *tree_lines,
        f"```",
    ]

    content = "\n".join(output_lines)

    # Печатаем в терминал
    print(content)

    # Сохраняем в файл
    OUTPUT_FILE.write_text(content, encoding="utf-8")
    print(f"\n✓ Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()