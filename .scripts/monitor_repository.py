import argparse
import dataclasses
import hashlib
import json
import logging
import subprocess
import tempfile
import tomllib
from functools import cache, cached_property
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Config:
    repo_url: str
    repo_branch: str
    original_link: str
    paths: list[tuple[str, str]]
    cache_file: Path

    @classmethod
    def from_config_file(cls, config_file_path: Path) -> 'Config':
        content = config_file_path.read_text()
        raw_config = tomllib.loads(content)

        logger.debug('Loaded config: %s', raw_config)

        return cls(
            repo_url=raw_config['repository']['repo_url'],
            repo_branch=raw_config['repository']['repo_branch'],
            original_link=raw_config['repository']['original_link'],
            paths=raw_config['repository']['paths'],
            cache_file=Path(raw_config['repository']['cache_file']),
        )


@dataclasses.dataclass
class CacheData:
    commit_hash: str | None
    file_hash: str | None


def read_files_json(path: Path) -> dict[str, CacheData]:
    if not path.exists():
        return {}
    raw_content = json.loads(path.read_text())
    return {
        key: CacheData(commit_hash=value.get('commit_hash'), file_hash=value.get('file_hash'))
        for key, value in raw_content.items()
    }


def write_files_json(path: Path, data: dict[str, CacheData]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    keys = sorted(data.keys())

    path.write_text(
        json.dumps(
            {key: {'commit_hash': data[key].commit_hash, 'file_hash': data[key].file_hash} for key in keys},
            indent=2,
        )
    )


@dataclasses.dataclass
class FileInfo:
    src: Path
    dst: Path

    _repo: 'GitRepository'

    def __hash__(self):
        return hash(f'{self.src}{self.dst}')

    @cached_property
    def file_hash(self) -> str:
        return hashlib.md5(self.src.read_bytes()).hexdigest()

    @cached_property
    def commit_hash(self) -> str:
        result = subprocess.run(
            ['git', 'rev-list', '-1', 'HEAD', '--', self.src.resolve()],
            cwd=self._repo.path,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()

    @cache
    def get_file_diff(
        self,
        old_commit: str,
    ) -> str:
        result = subprocess.run(
            ['git', 'diff', old_commit, self.commit_hash, '--', self.src.resolve()],
            cwd=self._repo.path,
            capture_output=True,
            text=True,
            check=True,
        )
        clear_result = result.stdout.strip()
        clear_result = '\n'.join(clear_result.split('\n')[4:])
        clear_result = f'{old_commit} -> {self.commit_hash}\n{clear_result}'
        return clear_result

    def copy(self) -> None:
        self.dst.parent.mkdir(parents=True, exist_ok=True)
        self.dst.write_text(self.src.read_text())


class GitRepository:
    def __init__(self, config: 'Config', path: Path) -> None:
        self.config = config
        self.path = path

    @classmethod
    def get(cls, config: 'Config', temp_dir: Path | None) -> 'GitRepository':
        if temp_dir is None:
            logger.info('Creating temporary directory')
            temp_dir = tempfile.mkdtemp()
            temp_dir = Path(temp_dir)

        logger.debug('Temporary directory: %s', temp_dir)

        if not temp_dir.exists() or not any(temp_dir.iterdir()):
            logger.debug('Cloning repository')
            subprocess.run(
                ['git', 'clone', config.repo_url, temp_dir.resolve()],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ['git', 'checkout', config.repo_branch],
                cwd=temp_dir,
                check=True,
                capture_output=True,
            )
            return cls(config, temp_dir)

        if any(temp_dir.iterdir()) and '.git' not in [x.name for x in temp_dir.iterdir()]:
            raise ValueError(f'{temp_dir} is not empty and not a git repository')

        check_result = subprocess.run(
            ['git', 'config', '--get', 'remote.origin.url'],
            cwd=temp_dir,
            capture_output=True,
            text=True,
        )
        if check_result.stdout.strip() != config.repo_url:
            raise ValueError(
                f'Expected repository url {config.repo_url}, got {check_result.stdout.strip()}'
            )

        subprocess.run(
            ['git', 'checkout', config.repo_branch],
            cwd=temp_dir,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ['git', 'pull'],
            cwd=temp_dir,
            check=True,
            capture_output=True,
        )
        return cls(config, temp_dir)

    def get_files_info(self) -> list[FileInfo]:
        file_infos: list[FileInfo] = []

        for src_raw, dst_raw in self.config.paths:
            src, dst = self.path / Path(src_raw), Path(dst_raw)
            if not src.exists():
                logging.warning(f'Path {src.resolve()} does not exist')
                continue
            if src.is_dir():
                for folder, _, files in src.walk():
                    for src_file in files:
                        src_file = Path(folder) / src_file
                        dst_file = dst / src_file.relative_to(src)
                        file_infos.append(FileInfo(src=src_file, dst=dst_file, _repo=self))
            else:
                src_file = self.path / Path(src_raw)
                dst_file = Path(dst_raw)
                file_infos.append(FileInfo(src=src_file, dst=dst_file, _repo=self))

        logger.debug('File infos: %s', file_infos)
        return file_infos

    def delete(self) -> None:
        logger.debug('Deleting folder %s', self.path)
        self.delete_folder(self.path)
        logger.debug('Folder %s deleted', self.path)

    def delete_folder(self, path: Path) -> None:
        for sub in path.iterdir():
            if sub.is_dir():
                self.delete_folder(sub)
            else:
                sub.unlink()
        path.rmdir()


def process_repository(
    save: bool, tmp_folder_path: Path | None, dry_run: bool, config_file: Path, cache_file: Path
) -> None:
    config = Config.from_config_file(config_file)
    files_cache = read_files_json(cache_file or config.cache_file)
    obsolete_files = set(files_cache.keys())

    changed_files: dict[Path, str] = {}

    repo = GitRepository.get(config, tmp_folder_path)

    file_infos = repo.get_files_info()

    for file_info in file_infos:
        file_cache_data = files_cache.get(str(file_info.dst))
        if file_cache_data is None:
            if not dry_run:
                file_info.copy()
            changed_files[file_info.dst] = 'New file'
        else:
            if file_cache_data.commit_hash != file_info.commit_hash:
                if file_cache_data.file_hash != file_info.file_hash:
                    if not dry_run:
                        file_info.copy()
                    changed_files[file_info.dst] = file_info.get_file_diff(
                        file_cache_data.commit_hash
                    )

        files_cache[str(file_info.dst)] = CacheData(
            commit_hash=file_info.commit_hash,
            file_hash=file_info.file_hash,
        )
        obsolete_files.discard(str(file_info.dst))

    for obsolete_file in obsolete_files:
        logging.info('Removing obsolete file %s', ', '.join(obsolete_file))
        del files_cache[obsolete_file]

    if not dry_run:
        logger.info('Writing cache file %s', cache_file)
        write_files_json(cache_file, files_cache)

    if changed_files:
        print(f'Sync with [original]({config.original_link})')
        for file, change in changed_files.items():
            change_message = change if change != 'New file' else 'New file'
            print(f' - `{file}`\n')
            print(f'```\n{change_message}\n```\n')

    if not save:
        logger.info('Deleting temporary folder %s', repo.path)
        repo.delete()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config',
        default='monitoring_config.toml',
        required=False,
        help='Path to the configuration file',
        type=Path,
    )
    parser.add_argument(
        '--cache',
        default='.files_cache.json',
        required=False,
        help='Path to the cache file',
        type=Path,
    )
    parser.add_argument(
        '--temp-folder',
        default=None,
        required=False,
        help='Temporary folder to store files',
        type=Path,
    )
    parser.add_argument(
        '-s',
        '--save',
        action='store_true',
        default=False,
        help='Save files in temporary folder',
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        default=False,
        help='Run without making changes',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=0,
    )
    args = parser.parse_args()
    verbose, save, temp_folder_path, dry_run = (
        args.verbose,
        args.save,
        args.temp_folder,
        args.dry_run,
    )
    config_file, cache_file = args.config, args.cache
    logging.basicConfig(level=(5 - verbose) * 10)

    logger.info('Processing repository')
    logger.debug('Running with params %s', ", ".join(f"{key}={value}" for key, value in vars(args).items()))

    process_repository(save, temp_folder_path, dry_run, config_file, cache_file)
