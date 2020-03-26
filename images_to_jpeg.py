# -*- coding: utf-8 -*-
import logging

import click
from p_tqdm import t_map
import multiprocessing as mp

from handler.file import all_files_in
from handler.image import is_image, convert_to_jpeg_and_override




@click.command()
@click.option("--path", "-i", type=click.Path(), required=True, help="path to open files from")
@click.option("--processes", "-p", type=int, default=2, required=True, help="nuber of processes to use. -1 all cores, 0 disables paralelism.")
def main(path, processes):
    logging.info(f"Looking for images. Please wait a moment.")
    files = all_files_in(path)
    images = [file for file in files if is_image(file)]
    logging.info(f"Converting {len(images)} to jpeg")

    if processes == 0:
        logging.info("Running normally")
        t_map(convert_to_jpeg_and_override, images)
    else:
        processes = mp.cpu_count() if processes == -1 else processes
        logging.info(f"Runnining using [{processes}] processes")
        pool = mp.Pool(mp.cpu_count())
        sults = pool.map(convert_to_jpeg_and_override, images)
        pool.close()

    logging.info("DONE")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
