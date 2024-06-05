import json
from pathlib import Path
from typing import Generator

from lucy.config.config import config
from lucy.filesystem import LocalFS


class SnippetOps:  # pylint: disable=too-few-public-methods

    @staticmethod
    def __generate_snippet(path: Path) -> tuple[str, dict[str, str | list[str]]]:
        filename = path.name
        name, ext = filename.split('.')
        scope = ext
        prefix = name
        body: list[str] = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip('\n')
                if filename != config.commons.template_file_name:
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

    @staticmethod
    def update() -> Generator[Path, None, None]:
        snippets = {}
        for file in LocalFS.get_snippet_files():
            yield file.relative_to(config.home)
            name, snippet = SnippetOps.__generate_snippet(file)
            snippets[name] = snippet
        with open(config.snippets.path, 'w', encoding='utf-8') as f:
            json.dump(snippets, f, indent=2)
