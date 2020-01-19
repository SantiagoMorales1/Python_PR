# -*- coding: utf-8 -*-
import click
import os
from PIL import Image
from handler.file import get_file_name, get_extension, walk_files, all_files_in
import logging


def is_image(filename_in):
    try:
        with Image.open(filename_in, mode='r') as _:
            logging.info(
                f"{filename_in} is a valid image with mode={_.mode} format={_.format} size=[width:{_.width}, \
				height:{_.height}] info={_.info}")
        return True
    except:
        logging.info(f"{filename_in} is NOT an image and will be skipped. ")
        return False


def try_read_image(filename_in):
    try:
        return Image.open(filename_in, mode='r')
    except:
        return None


def resize_with_aspect(im, filename_in, max_size):
    if max_size == im.size or max_size == (0, 0):
        logging.info(f"{filename_in} returning image as has correct size.")
        return im
    ratio = min(max_size[0] / im.width, max_size[1] / im.height)
    new_size = (int(ratio * im.width), int(ratio * im.height))
    logging.info(f"{filename_in} {im.size} will be changed to {new_size} @ ratio = {ratio}")
    resized = im.resize(new_size)
    return resized


def convert_to_jpeg(filename_in, filename_out, max_size=(0, 0), overwrite=False):
    logging.info(f"converting {filename_in} to jpeg")
    with Image.open(filename_in, mode='r') as im:
        rgb_im = im.convert('RGB') if im.mode != 'RGB' else im
        logging.info(f"{filename_in} >> {filename_out}")
        # if max_size != (0, 0):
        #	rgb_im = resize_with_aspect(rgb_im,filename_in, max_size)
        if overwrite:
            os.remove(filename_in)
        rgb_im.save(filename_out, "JPEG", optimize=True, quality=95)
    logging.info(f" wrote {filename_out}")


def get_target_jpeg(original_file, output_dir, extension=".jpg"):
    original_filename = os.path.basename(original_file)
    original_extension = get_extension(original_file)
    new_name = os.path.join(output_dir, original_filename.replace(original_extension, extension))
    return new_name


def get_target_jpeg_with_override(original_file, extension=".jpg"):
    original_name = get_file_name(original_file)
    new_name = original_name + ".jpg"
    return new_name


@click.command()
@click.option("--path", "-i", type=click.Path(), required=True, help="path to open files from")
@click.option("--output_dir", "-i", type=click.Path(), required=False, help="path to output files to")
# @click.option('--recursive', '-r', is_flag=True, help="Should it iterate deeper than the first level?")
@click.option('--max_size', '-s', type=click.Tuple([int, int]), default=(0, 0), help="resizing")
@click.option('--dry', '-d', is_flag=True, help="Convert the images to jpeg format and save them as 'jpg'.")
@click.option('--overwrite', '-o', is_flag=True, help="Overwrite current file.")
def main(path, output_dir, max_size, dry, overwrite):
    # list all files in folder
    files = all_files_in(path)
    # select images
    images = filter(is_image, files)

    for f in images:
        original = f
        target = get_target_jpeg_with_override(f) if overwrite else get_target_jpeg(f, output_dir)
        logging.info(f"{original} >> {target}")
        convert_to_jpeg(original, target, max_size=max_size, overwrite=overwrite)

    logging.info("DONE")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
