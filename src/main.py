import os.path
from pprint import pprint

import numpy as np
import matplotlib.pyplot as plt
import skimage.io as io

from glob import glob
from random import shuffle
from shutil import t


def parse_fddb_folds(path_dir_data="dataset/FDDB/data",
                     path_dir_folds="dataset/FDDB-folds/folds",
                     pattern_folds="FDDB-fold-*-ellipseList.txt",
                     extension_pictures="jpg", encoding="utf8",
                     newline="\n"):
    pictures = []
    print(path_dir_folds + "/" + pattern_folds)
    for path_folds in glob(path_dir_folds + "/" + pattern_folds):
        with open(path_folds, encoding=encoding, newline=newline) as file:
            path_picture = os.path.normpath(file.readline().strip())
            while path_picture != '.':
                picture = []
                for index_face in range(int(file.readline())):
                    face = file.readline().split()
                    picture.append({
                        "path": os.path.join(path_dir_data,
                                             path_picture + "." + extension_pictures),
                        "major_axis_radius": face[0],
                        "minor_axis_radius": face[1],
                        "angle": face[2],
                        "center_x": face[3],
                        "center_y": face[4],
                        "detection_score": face[5],
                    })
                pictures.append(picture)

                path_picture = os.path.normpath(file.readline().strip())
    return pictures
