# -*- coding: utf-8 -*-

import os
import shutil
from typing import List


def files_in(path: str, recursive=False, follow_symlinks=False):
    """
Lists all files in a given directory. It is possible to specify if
    :param path: Directory to list all files from.
    :param recursive: Traverse the directory recursively.
    :param follow_symlinks: Should symbolic links be followed?
    :return: Generator with file paths.
    """
    return walk_files(path=path, recursive=recursive, follow_symlinks=follow_symlinks)


def all_files_in(path: str) -> List[str]:
    """
Lists all files in a given directory. It will follow symbolic links and will operate recursively.
    :param path: Directory to list all files from.
    :return: Generator with file paths.
    """
    return files_in(path, recursive=True, follow_symlinks=True)


def walk_files_ext(path: str, ext: str, recursive: bool = False, follow_symlinks: bool = False):
    for file in walk_files(path=path, recursive=recursive, follow_symlinks=follow_symlinks):
        if file.endswith(ext):
            yield file


def walk_files(path: str, recursive: bool = True, follow_symlinks: bool = True):
    """
Lists all files in a given directory. It will follow symbolic links and will operate recursively.
    :param path: Directory to traverse.
    :param recursive: Should the directory be traversed recursively?
    :param follow_symlinks: Should symbolic links be followed?
    """
    if not os.path.isdir(path):
        raise NotADirectoryError(f"{path} is not a valid directory.")
    for entry in os.scandir(path):
        if entry.is_file():
            yield entry.path
        elif recursive and entry.is_dir(follow_symlinks=follow_symlinks):
            yield from walk_files(entry.path, recursive, follow_symlinks)


def get_extension(path: str) -> str:
    if os.path.exists(path) and os.path.isfile(path):
        _, file_extension = os.path.splitext(path)
        return file_extension


def get_file_name(path: str) -> str:
    if os.path.exists(path) and os.path.isfile(path):
        file_name, _ = os.path.splitext(path)
        return file_name


def move_to_dir(src_file, dest_dir):
    """
Moves the file to a specified directory. It will check that the specified directory exists and will create it if
necessary.
    :param src_file:
    :param dest_dir:
    """
    if not os.path.exists(src_file):
        raise FileNotFoundError(f"{src_file} does not exist and cannot be moved.")
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)
    shutil.move(src_file, dest_dir)


def remove_file_safely(path: str) -> None:
    """
Removes a file safely: checks if the file exists, and only then will it remove it.
    :param path:
    """
    if os.path.exists(path) and os.path.isfile(path):
        os.remove(path)


def create_folder(path: str) -> None:
    """
Creates a folder (thread safe).
    :param path:
    """
    os.makedirs(path, exist_ok=True)
