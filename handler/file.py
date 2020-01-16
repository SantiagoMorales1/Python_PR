# -*- coding: utf-8 -*-

import os
from typing import List


def files_in(path: str, recursive=False, follow_symlinks=False):
    return [file for file in walk_files(path=path, recursive=recursive,
                                        follow_symlinks=follow_symlinks)]


def all_files_in(path: str) -> List[str]:
    return files_in(path, True, True)


def walk_files_ext(path : str, ext: str, recursive=False) -> List[str]:
    for entry in os.scandir(path):
        if entry.is_file() and entry.name.endswith(ext):
            yield entry.path
        elif recursive and entry.is_dir(follow_symlinks=False):
            yield from walk_files_ext(entry.path, ext, recursive)


def walk_files(path: str, recursive=False, follow_symlinks=False):
    for entry in os.scandir(path):
        if entry.is_file():
            yield entry.path
        elif recursive and entry.is_file(follow_symlinks=follow_symlinks):
            yield from walk_files(entry.path, recursive, follow_symlinks)


def get_extension(path: str) -> str:
    if os.path.exists(path) and os.path.isfile(path):
        _, file_extension = os.path.splitext(path)
        return file_extension


def get_file_name(path: str) -> str:
    if os.path.exists(path) and os.path.isfile(path):
        file_name, _ = os.path.splitext(path)
        return file_name


def remove_file_safely(path: str) -> None:
    if os.path.exists(path) and os.path.isfile(path):
        os.remove(path)


def create_folder(path: str) -> None:
    os.makedirs(path, exist_ok=True)
