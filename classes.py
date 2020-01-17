# -*- coding: utf-8 -*-

from handler.file import all_files_in, walk_files
from typing import List
from handler.xml import class_xml_to_csv, xml_classes_dataframe, xml_callses_fix
from handler.image import is_image
from progress.bar import Bar
import pandas as pd
import numpy as np
import logging

import click  

def group_name(route, groups):
    for group in groups:
        if group in route:
            return group
    else:
        return None


def pre_process(path: str, groups: List[str]) -> pd.DataFrame:
    """[summary]
    
    Arguments:
        path {str} -- [description]
        groupos {List[str]} -- [description]
    """
    logging.info(f"Wroking on {path} and looking for groups {groups}")

    files = [f for f in all_files_in(path) ]
    xmls = [f for f in files if f.endswith(".xml")]
    images = [f for f in files if is_image(f)]
    updated_xmls = xml_callses_fix(xmls)

    num_xmls = len(xmls)
    num_images = len(images)
    num_files = len(files)
    num_updated_xmls = len(updated_xmls)

    logging.info(f"Found {num_files} files: {num_xmls} xmls (fixed {num_updated_xmls}) y {num_images} images")
    classes = xml_classes_dataframe(xmls)

    for group in groups:
        classes['_'+group] = classes['xmls_path'].apply(lambda x:  1 if group in x else 0)

    classes['group'] = classes['xmls_path'].apply(lambda x: group_name(x, groups))

    return classes


@click.command()
@click.option("--path", "-p", type=click.Path(), required=True, help="path to files -- Must exist")
@click.option("--frequencies", "-q", type=str, required=True, help="output file for csv -- Must not exist")
@click.option("--groups", "-g", type=click.Tuple([str,str]), default=("campo","estudio"), required=True, help="output file for csv -- Must not exist")
def main(path, frequencies, groups):
    classes = pre_process(path, groups)
    x = classes.groupby('class_name').count()['ref_image']

    logging.info("writting files")
    writer = pd.ExcelWriter(frequencies, engine='xlsxwriter')
    classes.to_excel(writer, sheet_name="data", index=False)
    x.to_excel(writer, sheet_name="classes_share", index=False)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
    

