# -*- coding: utf-8 -*-
import logging
import os
from functools import partial

import click

ITEM_ZFILL = 9
ITEM_FORMAT = """item {{\n\tid: {id}\n\tname: '{class_prefix}{class_name}'\n}}\n\n"""


def item_maker(id: int, class_prefix: str) -> str:
    item = dict(id=id, class_prefix=class_prefix,
                class_name=str(id).zfill(ITEM_ZFILL))
    return ITEM_FORMAT.format(**item)


def create_label_map(label_map_output: str, class_prefix: str, num_classes: int):
    ids = range(1, num_classes + 1)
    prefixed = partial(item_maker, class_prefix=class_prefix)
    items = map(prefixed, ids)
    with open(label_map_output, "w+", encoding="UTF-8", newline="\n") as label_map:
        label_map.writelines(items)
        label_map.close()
    assert(os.path.exists(label_map_output))


@click.command()
@click.option("--label_map_output", type=click.Path(file_okay=True, dir_okay=False, writable=True), required=True,
              help="Path to label_map")
@click.option("--class_prefix", required=True, help="Prefix for the class_name e.g. 'HN'.")
@click.option("--num_classes", type=click.INT, required=True, help="number of classes to generate.")
def main(label_map_output, class_prefix, num_classes):
    logging.info("BEGIN: label_map_maker")
    create_label_map(label_map_output, class_prefix, num_classes)
    logging.info("END: label_map_maker")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
