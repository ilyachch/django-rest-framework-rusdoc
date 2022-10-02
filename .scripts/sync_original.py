import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Tuple


class Tool:
    ORIGINAL_URL = 'https://github.com/encode/django-rest-framework.git'
    BASE_DIR = Path(__file__).resolve().parent.parent

    DATA_TO_WATCH = [
        (
            [
                Path('docs/api-guide/'),
            ],
            BASE_DIR / Path('.reference/api-navigation/'),
        ),
        (
            [
                Path('docs/tutorial/'),
                Path('docs/coreapi/'),
            ],
            BASE_DIR / Path('.reference/quick-start/'),
        ),
        (
            [
                Path('docs/topics/'),
            ],
            BASE_DIR / Path('.reference/topics/'),
        ),
        (
            [
                Path('docs/index.md'),
            ],
            BASE_DIR / Path('.reference/README.md'),
        ),
    ]

    def __init__(self) -> None:
        self._temp_dir: Path = self._get_temp_dir()

    def _get_temp_dir(self) -> Path:
        temp_dir = tempfile.mkdtemp()
        return Path(temp_dir)

    def clone(self) -> None:
        self._temp_dir.mkdir(parents=True, exist_ok=True)
        if self._temp_dir.exists() and '.git' in self._temp_dir.iterdir():
            subprocess.run(['git', 'pull'], cwd=self._temp_dir, check=True, capture_output=True)
        else:
            subprocess.run(['git', 'clone', self.ORIGINAL_URL, self._temp_dir], check=True, capture_output=True)

    def make_list_of_files_to_copy(self) -> List[Tuple[Path, Path]]:
        files_to_copy = []
        for sources, target in self.DATA_TO_WATCH:
            for source in sources:
                updated_source = self._temp_dir / source
                if updated_source.is_dir():
                    files_in_source = list(updated_source.glob('*.md'))
                    for file_ in files_in_source:
                        files_to_copy.append((file_, target))
                else:
                    files_to_copy.append((updated_source, target))
        return files_to_copy

    def copy_file(self, source: Path, target: Path, make_hash: bool = True) -> None:
        if target.suffix == '.md':
            target_file = self.BASE_DIR.joinpath(target)
        else:
            target_file = self.BASE_DIR.joinpath(target, source.name)
        target_file.parent.mkdir(parents=True, exist_ok=True)
        if not target_file.exists():
            target_file_path = target_file.parent
            target_file_path.mkdir(parents=True, exist_ok=True)
        target_file.write_text(source.read_text())
        if make_hash:
            self.make_hash(target_file)

    def make_hash(self, file_: Path) -> None:
        hash_file_name = file_.name + '.hash'
        file_hash = hashlib.md5(file_.read_bytes()).hexdigest()
        hash_file = self.BASE_DIR.joinpath(file_.parent, hash_file_name)
        if hash_file.exists():
            existing_hash = hash_file.read_text()
            if existing_hash == file_hash:
                return
            print(file_.relative_to(self.BASE_DIR))
        else:
            print(file_.relative_to(self.BASE_DIR))
        hash_file.write_text(file_hash)

    def clean(self) -> None:
        self.delete_folder(self._temp_dir)

    def delete_folder(self, path: Path) -> None:
        for sub in path.iterdir():
            if sub.is_dir():
                self.delete_folder(sub)
            else:
                sub.unlink()
        path.rmdir()

    def run(self) -> None:
        self.clone()
        files_to_copy = self.make_list_of_files_to_copy()
        for source, target in files_to_copy:
            self.copy_file(source, target)
        self.clean()


if __name__ == '__main__':
    Tool().run()
