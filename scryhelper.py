# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 04:21:11 2021

@author: sergey
"""

from IPython.core.display import display
from PIL import Image
from pathlib import Path
from random import randint
from math import log10, ceil
import re
import requests

FUNQ = "is:funny include:extra"
MAXRAND = 99999
RAND_DIGITS = ceil(log10(MAXRAND+1))
SAVEDIR = Path("./cards")

def save_random_card(q='', additional_params={}):
    print(additional_params, q)
    if 'q' in additional_params:
        print('save_random_card(): additional_params cannot have key "q"')
        return
    additional_params['q'] = q
    random_card = requests.get(url="https://api.scryfall.com/cards/random", params=additional_params, timeout=1).json()
    del additional_params
    image_uri = random_card["image_uris"]["normal"]
    card_image = Image.open(requests.get(image_uri, stream=True).raw)
    display(card_image)
    filename = random_card["name"].replace(" ", "_").replace("/", ":") + ".jpg"
    
    if 'y' == input('Save image to file (y/[n])? '):
        SAVEDIR.mkdir(parents=True, exist_ok=True)
        target_filename = SAVEDIR/filename
        card_image.convert('RGB').save(target_filename)
        print(f'Successfully saved to file "{target_filename}".')

def rotate_dir_images(cw = True, path=SAVEDIR):
    rotation = Image.ROTATE_270 if cw else Image.ROTATE_90
    for image in path.iterdir():
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
