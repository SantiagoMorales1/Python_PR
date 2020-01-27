# -*- coding: utf-8 -*-
import logging

import click
from tqdm import tqdm

from handler.file import all_files_in
from handler.image import is_image, convert_to_jpeg_and_override


@click.command()
@click.option("--path", "-i", type=click.Path(), required=True, help="path to open files from")
def main(path):
    files = all_files_in(path)
    images = [file for file in files if is_image(file)]
    logging.info(f"Converting {len(images)} to jpeg")

    for image in tqdm(images, desc="converting to JPEG"):
        convert_to_jpeg_and_override(image)  # TODO: Paralelizar esto. multiprocessing, joblib, o ray

    logging.info("DONE")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
