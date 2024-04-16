import argparse
import hashlib
import logging
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

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


@dataclass
class DataMap:
    source: Path
    target: Path

    def update_source_with_base(self, base: Path) -> None:
        self.source = base / self.source

    def source_is_dir(self) -> bool:
        return self.source.is_dir()

    def __iter__(self):
        if self.source_is_dir():
            for file in self.source.iterdir():
                if file.suffix == '.md':
                    yield file
        else:
            yield self.source


class Tool:
    ORIGINAL_URL = 'https://github.com/encode/django-rest-framework.git'
    BASE_DIR = Path(__file__).resolve().parent.parent

    DATA_TO_WATCH: List[DataMap] = [
        DataMap(Path('docs/api-guide/'), BASE_DIR / Path('.reference/api-guide/')),
        DataMap(Path('docs/tutorial/'), BASE_DIR / Path('.reference/tutorial/')),
        DataMap(Path('docs/coreapi/'), BASE_DIR / Path('.reference/tutorial/')),
        DataMap(Path('docs/topics/'), BASE_DIR / Path('.reference/topics/')),
        DataMap(Path('docs/index.md'), BASE_DIR / Path('.reference/README.md')),
    ]

    def __init__(self, tmp_folder: Optional[str] = None, tmp_save: bool = False, dry_run: bool = False) -> None:
        self._temp_dir: Path = Path(tmp_folder) if tmp_folder else Path(tempfile.mkdtemp())
        self._save = tmp_save
        self._dry_run = dry_run
        for data_map in self.DATA_TO_WATCH:
            data_map.update_source_with_base(self._temp_dir)

    def get_latest_original(self) -> None:
        self._temp_dir.mkdir(parents=True, exist_ok=True)
        logger.info(self._temp_dir.resolve())
        logger.debug('folder exists: %s', self._temp_dir.exists())
        logger.debug('folder contents: %s', ', '.join(str(x) for x in self._temp_dir.iterdir()))
        if self._temp_dir.exists() and self._temp_dir / '.git' in self._temp_dir.iterdir():
            logger.info('Updating original')
            subprocess.run(['git', 'pull'], cwd=self._temp_dir, check=True, capture_output=True)
        else:
            logger.info('Cloning original')
            subprocess.run(['git', 'clone', self.ORIGINAL_URL, self._temp_dir], check=True, capture_output=True)

    def make_list_of_files_to_copy(self) -> List[Tuple[MdFile, MdFile]]:
        files_to_copy = []
        for data_map in self.DATA_TO_WATCH:
            if not data_map.source.exists():
                logger.warning('Path %s does not exist', data_map.source.resolve())
                continue
            if data_map.source_is_dir():
                for source_file in data_map:
                    target = data_map.target / source_file.name
                    logger.debug('source_file: %s', source_file)
                    logger.debug('target_file: %s', target)
                    files_to_copy.append((MdFile(source_file), MdFile(target)))
            else:
                files_to_copy.append((MdFile(data_map.source), MdFile(data_map.target),) )
        logger.info('Found %d files to copy', len(files_to_copy))
        for source, target in files_to_copy:
            logger.info('%s -> %s', source, target)
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
        if not self._dry_run:
            target.write_text(source.read_text())
            target.hash_file.write_text(source.hash)
        print(target.relative_to(self.BASE_DIR))

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
            pass
            # print(f'Files are saved in: {self._temp_dir.resolve()}')
        else:
            self.clean()
        logger.info('Finished sync')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('temp_folder', nargs='?', default=None)
    parser.add_argument('-s', '--save', action='store_true', default=False)
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('--dry-run', action='store_true', default=False)
    args = parser.parse_args()
    verbose, save, temp_folder, dry_run = args.verbose, args.save, args.temp_folder, args.dry_run
    logging.basicConfig(level=(5 - verbose) * 10)
    Tool(tmp_folder=temp_folder, tmp_save=save, dry_run=dry_run).run()
