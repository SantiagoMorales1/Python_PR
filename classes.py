# -*- coding: utf-8 -*-
from handler.file import all_files_in, walk_files
from typing import List, Tuple
from handler.xml import class_xml_to_csv, xml_classes_dataframe, xml_callses_fix
from handler.image import is_image
from progress.bar import Bar
import pandas as pd
import numpy as np
import logging
import click


def group_name(route: str, groups: Tuple[str, str]):
    current = "DEFAULT"
    for group in groups:
        if group in route:
            current = group
    return current


def check_bbox_size(row, tolerance=33):
    x_value = row['xmax'] - row['xmin']
    y_value = row['ymax'] - row['ymin']
    if x_value < tolerance or y_value < tolerance or \
            row['xmin'] > row['width'] or \
            row['xmax'] > row['width'] or \
            row['ymax'] > row['height'] or \
            row['ymin'] > row['height']:
        return 1
    else:
        return 0


def to_frequencies(df: pd.DataFrame) -> pd.DataFrame:
    df['unit'] = 1
    df['class_name'] = df['class_name'].astype("category")
    df['group'] = df['group'].astype("category")
    table = pd.pivot_table(df, index=["class_name"],
                           columns=['group'],
                           values=['unit'],
                           aggfunc='count',
                           fill_value=0,
                           margins=True)
    return table


def pre_process(path: str, groups: List[str]) -> pd.DataFrame:
    """[summary]
    Arguments:
        path {str} -- [description]
        groupos {List[str]} -- [description]
    """
    logging.info(f"Wroking on {path} and looking for groups {groups}")

    files = [f for f in all_files_in(path)]
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
        classes['_' + group] = classes['xmls_path'].apply(lambda x: 1 if group in x else 0)

    classes['group'] = classes['xmls_path'].apply(lambda x: group_name(x, groups))
    classes['bboxes'] = classes.apply(check_bbox_size, axis=1)
    freq = to_frequencies(classes)

    return classes, freq


@click.command()
@click.option("--path", "-p", type=click.Path(), required=True, help="path to files -- Must exist")
@click.option("--frequencies", "-q", type=str, required=True, help="output file for csv -- Must not exist")
@click.option("--to_excel", "-e", type=str, required=False, help="output file for excel -- Must not exist")
@click.option("--groups", "-g", type=click.Tuple([str, str]), default=("campo", "estudio"), required=True,
              help="output file for csv -- Must not exist")
def main(path, frequencies, to_excel, groups):
    classes, freq = pre_process(path, groups)
    x = classes.groupby('class_name').count()[['xmls_path']]
    dgroups = {k: 0 for k in groups}
    dgroups['All'] = 0
    logging.info("writting files")
    logging.info(f"CSV > {frequencies}")
    classes.to_csv(frequencies, index=False)

    logging.info(f"XLSX > {to_excel}")

    writer = pd.ExcelWriter(to_excel, engine='xlsxwriter')
    classes.to_excel(writer, sheet_name="data")
    x.to_excel(writer, sheet_name="prescence")
    freq.to_excel(writer, sheet_name="frequencies")
    writer.save()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
