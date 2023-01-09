# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 18:22:00 2023

@author: sergey
"""
from PIL import Image
from pathlib import Path
from math import log10, ceil
from random import randint
from os import getcwd
import re


MAXRAND = 99
RAND_DIGITS = ceil(log10(MAXRAND+1))
SAVEDIR = Path(getcwd()) / Path("cards")


def rotate_dir_images(cw=True, path=SAVEDIR):
    path = Path(path)
    rotation = Image.ROTATE_270 if cw else Image.ROTATE_90 # Rotation is inverse
    for image in filter(Path.is_file, path.iterdir()):
        Image.open(image).transpose(rotation).save(image)

def shuffle_dir(path=SAVEDIR):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    for image in path.iterdir():
        image.rename(path / add_rand(image.name))

def unshuffle_dir(path=SAVEDIR):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    for image in path.iterdir():
        image.rename(path / remove_rand(image.name))

def add_rand(name):
    name = str(name)
    regex = r"^(\d+%)*"
    prefix = f'%0{RAND_DIGITS}d%%' % randint(0, MAXRAND) 
    return re.sub(regex, prefix, name)

def remove_rand(name):
    regex = r"^(\d+%)*"
    return re.sub(regex, '', name)