import json
import os
from typing import Generator


def files(path: str) -> Generator[str, None, None]:
    for entry in os.scandir(path):
        if entry.is_file():
            yield entry.path
        elif entry.is_dir():
            yield from files(entry.path)


def generate_snippet(path: str) -> tuple[str, dict[str, str | list[str]]]:
    filename = os.path.basename(path)
    name, ext = filename.split('.')
    scope = ext
    prefix = name
    body: list[str] = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip('\n')
            if name != 'base':
                if line.startswith(('#include', 'using')):
                    if not line.endswith('//'):
                        continue
                if not body and not line:
                    continue
            body.append(line)
    return name, {
        'scope': scope,
        'prefix': prefix,
        'body': body,
    }


def run(entry_dir: str, snippet_file: str) -> list[str]:
    snippets = {}
    snippet_files = []
    for file in files(entry_dir):
        snippet_files.append(file)
        name, snippet = generate_snippet(file)
        snippets[name] = snippet
    with open(snippet_file, 'w', encoding='utf-8') as f:
        json.dump(snippets, f, indent=2)
    return snippet_files
