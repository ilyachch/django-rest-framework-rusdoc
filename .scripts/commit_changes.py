#!/usr/bin/env python3

import argparse
import dataclasses
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class FileStatus:
    status: str
    path: Path

    @property
    def is_modified(self) -> bool:
        return "M" in self.status

    @property
    def is_deleted(self) -> bool:
        return "D" in self.status

    @property
    def is_in_reference(self) -> bool:
        return str(self.path).startswith(".reference/")


def run_command(command: List[str], cwd: Path | None = None) -> str:
    """Выполняет команду и возвращает результат"""
    logger.debug(f"Running command: {' '.join(command)}")
    process = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if process.returncode != 0:
        raise RuntimeError(f"Command failed: {process.stderr}")
    return process.stdout.strip()


def get_git_status() -> str:
    """Получает статус git в формате porcelain"""
    return run_command(["git", "status", "--porcelain"])


def parse_status_line(line: str) -> FileStatus | None:
    """Разбирает строку статуса git и возвращает FileStatus"""
    if not line:
        return None

    # Формат вывода git status --porcelain:
    # XY PATH или XY "PATH с пробелами"
    parts = line.split(maxsplit=1)
    if len(parts) != 2:
        return None

    status = parts[0].strip()
    file_path = parts[1].strip()

    return FileStatus(status=status, path=Path(file_path))


def get_file_pairs() -> List[Tuple[Path, Path]]:
    """
    Находит пары файлов:
    - измененный файл в корне
    - удаленный файл в .reference с тем же относительным путем
    """
    status_output = get_git_status()

    modified_files: Dict[Path, FileStatus] = {}
    deleted_reference_files: Dict[Path, FileStatus] = {}

    for line in status_output.split("\n"):
        if not line:
            continue

        file_status = parse_status_line(line)
        if not file_status:
            continue

        # Измененные файлы (не в .reference)
        if file_status.is_modified and not file_status.is_in_reference:
            modified_files[file_status.path] = file_status

        # Удаленные файлы в .reference
        if file_status.is_deleted and file_status.is_in_reference:
            deleted_reference_files[file_status.path] = file_status

    # Находим пары файлов
    file_pairs = []
    for modified_path, status in modified_files.items():
        reference_path = Path(".reference") / modified_path

        if reference_path in deleted_reference_files:
            file_pairs.append((modified_path, reference_path))
        else:
            logger.warning(f"No matching deleted reference file for {modified_path}")

    return file_pairs


def commit_file_pair(
    modified_file: Path, reference_file: Path, dry_run: bool = False
) -> None:
    """Создает коммит для пары файлов"""
    file_name = modified_file.name
    commit_message = f"update {file_name}"

    logger.info(f"Committing changes for {file_name}...")

    if dry_run:
        logger.info(f"[DRY RUN] Would add: {modified_file} {reference_file}")
        logger.info(f"[DRY RUN] Would commit with message: {commit_message}")
        return

    # Добавляем файлы в индекс
    run_command(["git", "add", str(modified_file), str(reference_file)])

    # Создаем коммит
    run_command(["git", "commit", "-m", commit_message])

    logger.info(f"Committed: {commit_message}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create separate commits for each pair of related files"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Run without making actual commits",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (can be used multiple times)",
    )

    args = parser.parse_args()

    dry_run, verbose = args.dry_run, args.verbose

    log_level = (5 - verbose) * 10
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    logger.info("Starting file pair commit process")
    logger.debug(f"Arguments: dry_run={dry_run}, verbose={verbose}")

    try:
        file_pairs = get_file_pairs()

        if not file_pairs:
            logger.warning("No matching file pairs found")
            return

        logger.info(f"Found {len(file_pairs)} file pairs to commit")

        for modified_file, reference_file in file_pairs:
            commit_file_pair(modified_file, reference_file, dry_run)

        logger.info("All commits created successfully!")

    except Exception as e:
        logger.error(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
