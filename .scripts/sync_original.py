import hashlib
import logging
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Tuple, Optional
import argparse

logger = logging.getLogger(__name__)


class MdFile(type(Path())):
    def _make_hash(self) -> str:
        return hashlib.md5(self.read_bytes()).hexdigest()

    @property
    def hash(self) -> str:
        if not hasattr(self, '_hash'):
            self._hash = self._make_hash()
        return self._hash

    @property
    def hash_file(self) -> Path:
        return self.with_name(self.name + '.hash')


class Tool:
    ORIGINAL_URL = 'https://github.com/encode/django-rest-framework.git'
    BASE_DIR = Path(__file__).resolve().parent.parent

    DATA_TO_WATCH: List[Tuple[List[Path], Path]] = [
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

    def __init__(self, temp_folder: Optional[str] = None, save: bool = False) -> None:
        self._temp_dir: Path = Path(temp_folder) if temp_folder else Path(tempfile.mkdtemp())
        self._save = save

    def get_latest_original(self) -> None:
        self._temp_dir.mkdir(parents=True, exist_ok=True)
        logger.info(self._temp_dir.resolve())
        logger.debug('folder exists: %s', self._temp_dir.exists())
        logger.debug('folder contents: %s', list(self._temp_dir.iterdir()))
        if self._temp_dir.exists() and self._temp_dir / '.git' in self._temp_dir.iterdir():
            logger.info('Updating original')
            subprocess.run(['git', 'pull'], cwd=self._temp_dir, check=True, capture_output=True)
        else:
            logger.info('Cloning original')
            subprocess.run(['git', 'clone', self.ORIGINAL_URL, self._temp_dir], check=True, capture_output=True)

    def make_list_of_files_to_copy(self) -> List[Tuple[MdFile, MdFile]]:
        files_to_copy = []
        for sources, target in self.DATA_TO_WATCH:
            for source in sources:
                updated_source = self._temp_dir / source
                if not updated_source.exists():
                    logger.warning('Path %s does not exist', updated_source.resolve())
                    continue

                if updated_source.is_dir():
                    files_in_source = list(updated_source.glob('*.md'))
                    for source_file in files_in_source:
                        if target.is_dir():
                            target_file = target / source_file.name
                        else:
                            target_file = target
                        logger.debug('source_file: %s', source_file)
                        logger.debug('target_file: %s', target_file)
                        files_to_copy.append((MdFile(source_file), MdFile(target_file)))
                elif updated_source.is_file():
                    source_file = updated_source
                    if target.is_dir():
                        target_file = target / updated_source.name
                    else:
                        target_file = target
                    logger.debug('source_file: %s', source_file)
                    logger.debug('target_file: %s', target_file)
                    files_to_copy.append((MdFile(source_file), MdFile(target_file)))
                else:
                    raise ValueError('Unknown type of path: %s', updated_source)
        logger.info(
            f'Found %d files to copy: %s',
            len(files_to_copy),
            ', '.join([f'{source} -> {target}' for source, target in files_to_copy]),
        )
        return files_to_copy

    def copy_file(self, source: MdFile, target: MdFile) -> None:
        if not target.parent.exists():
            logger.info('Creating folder %s', target.parent)
            target.parent.mkdir(parents=True, exist_ok=True)
        if target.hash_file.exists():
            logger.debug('target.hash_file: %s', target.hash_file)
            logger.debug('target.hash_file.read_text(): %s', target.hash_file.read_text())
            logger.debug('source.hash: %s', source.hash)
            if source.hash == target.hash_file.read_text():
                logger.info('File %s is up to date', target)
                return
        logger.info('Updating file %s', target)
        target.write_text(source.read_text())
        target.hash_file.write_text(source.hash)

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
        logger.info('Starting sync')
        self.get_latest_original()
        files_to_copy = self.make_list_of_files_to_copy()
        for source, target in files_to_copy:
            self.copy_file(source, target)
        if self._save:
            print(f'Files are saved in: {self._temp_dir.resolve()}')
        else:
            self.clean()
        logger.info('Finished sync')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('temp_folder', nargs='?', default=None)
    parser.add_argument('-s', '--save', action='store_true', default=False)
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    verbose, save, temp_folder = args.verbose, args.save, args.temp_folder
    logging.basicConfig(level=(5 - verbose) * 10)
    Tool(temp_folder=temp_folder, save=save).run()
