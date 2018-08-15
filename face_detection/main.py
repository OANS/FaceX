import os.path
from pprint import pprint

import numpy as np
import matplotlib.pyplot as plt
import skimage.io as io

from glob import glob
from random import shuffle
from shutil import copyfile


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

def main():
    #laod dataset
    pictures_data = parse_fddb_folds("dataset/originalPics", "dataset/FDDB-folds")
    dict_pictures = {}
    for d in pictures_data: #gather all the faces of the same picture
        print(d[0]["path"])
        if d[0]["path"] in dict_pictures:
            dict_pictures[d[0]["path"]].append(d)
        else:
            dict_pictures[d[0]["path"]] = [d]
    pictures = list(dict_pictures.keys())
    print(len(pictures))
    #shuffle and split dataset
    shuffle(pictures)
    train = pictures[:int(len(pictures) * .6)]
    valid = pictures[int(len(pictures) * .6):int(len(pictures) * .8)]
    test  = pictures[int(len(pictures) * .8):]
    print(len(train), len(valid), len(test))
    #save the folds
    data_splits = [('train', train), ('valid', valid), ('test', test)]
    for dir_name, image_paths in data_splits:
        print("making {} ...".format(dir_name))
        #create the dir if not exists
        try: os.mkdir("dataset/" + dir_name)
        except: pass
        #save the images
        for image_path in image_paths:
            #copy the image
            print(dict_pictures[image_path][0])
            for i in range(len(dict_pictures[image_path][0])):
                copyfile(
                    dict_pictures[image_path][0][i]["path"], 
                    "dataset/{}/".format(dir_name) + dict_pictures[image_path][0][i]["path"].split('/')[-1]
                ) 
                #save the faces info of the image
                s = ""
                for f in dict_pictures[image_path][0]:
                    s += "{} {} {} {} {}".format(
                        f["major_axis_radius"],
                        f["minor_axis_radius"],
                        f["angle"],
                        f["center_x"],
                        f["center_y"]
                    ) + '\n'
                faces_info = open("dataset/{}/".format(dir_name) + dict_pictures[image_path][0][i]["path"].split('/')[-1] + '.txt', 'w')
                faces_info.write(s)
                faces_info.close()


if __name__ == '__main__':
    main()
