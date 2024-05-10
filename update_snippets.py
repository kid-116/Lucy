import json
import os
from typing import Generator

file_dir = os.path.dirname(__file__)
ENTRY_DIR = f'{file_dir}/common'
SNIPPET_FILE = f'{file_dir}/.vscode/cp.code-snippets'


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
    body = []
    with open(path, 'r') as f:
        for line in f:
            body.append(line.strip('\n'))
    return name, {
        'scope': scope,
        'prefix': prefix,
        'body': body,
    }


def main() -> None:
    snippets = {}
    for file in files(ENTRY_DIR):
        name, snippet = generate_snippet(file)
        snippets[name] = snippet
    json.dump(snippets, open(SNIPPET_FILE, 'w'))


if __name__ == '__main__':
    main()
