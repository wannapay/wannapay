import os
import wget
from PIL import Image
from db import img

prefix = 'https://www.ppshk.com/hkt/revamp2/Chinese/images/'

def prepare_images():
    for item in img.items():
        if not os.path.isfile(item[1]['name']):
            wget.download(prefix+item[1]['src'])
            with Image.open(item[1]['src']) as src:
                if 'crop' in item[1]:
                    cropped = src.crop(item[1]['crop'])
                    cropped.save(item[1]['name'])
                else:
                    Image.open(item[1]['src']).convert('RGB').save(item[1]['name'])
            os.remove(item[1]['src'])
