# -*- coding: utf-8 -*-
import ntpath
import os
import xml.etree.ElementTree as ET

import click
import pandas as pd
from PIL import Image

IN_DIR = ""
column_name = ['img_path', 'xml_path', 'filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']


def image_size(path):
	try:
		if not os.path.isfile(path):
			path = _find_file(path)
		with Image.open(path) as img:
			return img.size
	except:
		# _find_file(path_leaf(path))
		return 0, 0


def get_side_jpeg(xml_path) -> str:
	return str(xml_path).replace(".xml", '.jpg')


def xml_csv(xml_file):
	tree = ET.parse(xml_file)
	root = tree.getroot()
	img_file = get_side_jpeg(xml_file)  # os.path.join(folder, root.find('filename').text)
	width, height = image_size(img_file)
	for member in root.findall('object'):
		yield (img_file,
			   xml_file,
			   root.find('filename').text,
			   width,
			   height,
			   member[0].text,
			   int(member[4][0].text),
			   int(member[4][1].text),
			   int(member[4][2].text),
			   int(member[4][3].text)
			   )


def _find_file(path):
	name = path_leaf(path)
	for entry in os.scandir(IN_DIR):
		if entry.is_file() and entry.name == name:
			return entry.name


def path_leaf(path):
	head, tail = ntpath.split(path)
	return tail or ntpath.basename(head)


def walk_files(path, ext, recursive=False):
	for entry in os.scandir(path):
		if entry.is_file() and entry.name.endswith(ext):
			yield entry.path
		elif recursive and entry.is_dir(follow_symlinks=False):
			yield from walk_files(entry.path, ext, recursive)


def secure_out_file(file):
	if os.path.exists(file):
		raise FileExistsError()


def secure_in_dir(path):
	if not os.path.exists(path) or not os.path.isdir(path):
		raise NotADirectoryError


@click.command()
@click.option("--in_path", "-i", type=click.Path(), required=True, help="path to files")
@click.option("--out_path", "-o", type=str, required=True, help="output file for csv")
@click.option('--recursive', '-r', is_flag=True, help="recursive")
@click.option('--crop', '-c', is_flag=True, help="crop")
def main(in_path, out_path, recursive, crop):
	secure_in_dir(in_path)
	secure_out_file(out_path)
	ext = "xml"
	global IN_DIR
	IN_DIR = in_path
	val_list = []
	for file in walk_files(in_path, ext, recursive):
		for val in xml_csv(file):
			val_list.append(val)
	xml_df = pd.DataFrame(val_list, columns=column_name)
	xml_df.to_csv(out_path, ",", "", index=True, encoding="UTF-8")


if __name__ == '__main__':
	main()
