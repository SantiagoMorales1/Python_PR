# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from handler.file import get_file_name
from handler.image import image_size
from typing import Tuple, NamedTuple, List
from progress.bar import Bar
import pandas as pd
import os
import logging


def read_xml(xml_file: str):
    return ET.parse(xml_file)


COLUMNS = ["image_path", "xmls_path", "ref_image", "width", \
           "height", "class_name", "xmin", "ymin", "xmax", "ymax"]


def class_xml_to_csv(xml_file: str) -> \
        Tuple[str, str, str, int, int, str, int, int, int, int]:
    root = read_xml(xml_file).getroot()
    img_file = get_file_name(xml_file) + ".jpg"
    width, height = image_size(img_file)
    file_name = root.find('filename').text
    return [(img_file,
             xml_file,
             file_name,
             width,
             height,
             member[0].text,
             int(member[4][0].text),
             int(member[4][1].text),
             int(member[4][2].text),
             int(member[4][3].text)
             ) for member in root.findall("object")]


def xml_classes_dataframe(xmls):
    csv = []
    with Bar('Creating df', max=len(xmls)) as bar:
        for xml in xmls:
            csv += class_xml_to_csv(xml)
            bar.next()
    df = pd.DataFrame(csv, columns=COLUMNS)
    return df


def xml_callses_fix(xmls):
    fixed = []
    with Bar('fixing xmls', max=len(xmls)) as bar:
        for xml in xmls:
            if fix_reference_filename(xml):
                fixed += xmls
            bar.next()
    return fixed


def freq_nodes(xmls: List[str]):
    dict = {}
    for f in xmls:
        root = read_xml(f).getroot()
        for o in root.findall("object"):
            clase = o[0].text
            if clase in dict:
                dict[clase] += 1
            else:
                dict[clase] = 1
    return dict


def fix_reference_filename(xml_file: str) -> bool:
    tree = read_xml(xml_file)
    root = tree.getroot()
    original = root.find('filename').text
    expected = os.path.basename(xml_file).replace(".xml", ".jpg")
    if original != expected:
        root.find('filename').text = expected
        tree.write(xml_file)
        logging.info(f" update_path --> {xml_file} [{original}]>>[{expected}]")
        return True
    return False
