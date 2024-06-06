import json
import os
from pathlib import Path
from typing import Generator

from lucy.config.config import config


class SnippetOps:  # pylint: disable=too-few-public-methods

    def __generate_snippet(self, path: Path) -> tuple[str, dict[str, str | list[str]]]:
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

    def __get_snippet_files(self, path: Path = config.commons.dir_) -> Generator[Path, None, None]:
        for entry in os.scandir(path):
            entry_path = Path(entry.path)
            if entry.is_file():
                yield entry_path
            elif entry.is_dir():
                yield from self.__get_snippet_files(entry_path)

    def update(self) -> Generator[Path, None, None]:
        snippets = {}
        for file in self.__get_snippet_files():
            yield file.relative_to(config.home)
            name, snippet = self.__generate_snippet(file)
            snippets[name] = snippet
        with open(config.snippets.path, 'w', encoding='utf-8') as f:
            json.dump(snippets, f, indent=2)

    def create_global_snippets_link(self, force: bool = False) -> bool:
        link_absent = not config.snippets.global_link.exists()
        if link_absent or force:
            if not link_absent:
                os.remove(config.snippets.global_link)
            os.symlink(config.snippets.path, config.snippets.global_link)
        return not link_absent
