# -*- coding: utf-8 -*-

from handler.file import all_files_in


def frequencies(path):
	files = all_files_in(path)
	xmls = filter(files, lambda)
