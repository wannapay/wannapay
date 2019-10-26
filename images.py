##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <https://www.gnu.org/licenses/>.


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
