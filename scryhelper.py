# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 04:21:11 2021

@author: sergey
"""

from IPython.core.display import display
from PIL import Image
from pathlib import Path
from math import log10, ceil
from sys import argv
from os import getcwd
import requests

FUNQ = "is:funny include:extra"
TIMEOUT = 3
MAXRAND = 99
RAND_DIGITS = ceil(log10(MAXRAND+1))
SAVEDIR = Path(getcwd()) / Path("cards")

def main(argv=argv):
    if len(argv)>1:
        save_random_card(q=argv[1])

def save_random_card(q='', additional_params={}):
    if 'q' in additional_params:
        print('save_random_card(): additional_params cannot have key "q"')
        return
    params = additional_params.copy()
    params['q'] = q
    random_card = requests.get(url="https://api.scryfall.com/cards/random", params=params, timeout=TIMEOUT).json()
    image_uri = random_card["image_uris"]["normal"]
    card_image = Image.open(requests.get(image_uri, stream=True).raw)
    display(card_image)
    filename = random_card["name"].replace(" ", "_").replace("/", "%") + ".jpg"
    
    if 'y' == input(f'Save image of {random_card["name"]} to file (y/[n])? '):
        SAVEDIR.mkdir(parents=True, exist_ok=True)
        target_filename = SAVEDIR/filename
        card_image.convert('RGB').save(target_filename)
        print(f'Successfully saved to file "{target_filename}".')

def print_random_card(q='', additional_params={}):
    if 'q' in additional_params:
        print('save_random_card(): additional_params cannot have key "q"')
        return
    params = additional_params.copy()
    params['q'] = q
    random_card = requests.get(url="https://api.scryfall.com/cards/random", params=params, timeout=TIMEOUT).json()
    image_uri = random_card["image_uris"]["normal"]
    card_image = Image.open(requests.get(image_uri, stream=True).raw)
    display(card_image)
    

if __name__ == '__main__':
    main()
