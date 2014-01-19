# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# pynbome library
# lsd.py (c) Mikhail Mezyakov <mihail265@gmail.com>
#
# Compose source image with pattern

from wand.image import Image

def apply_filter(img):
  
    fg_filename = 'data/lsd.png'
    fg_img = Image(filename=fg_filename)
    
    width, height = fg_img.size
    img.resize(width)
    img.crop(width=width, height=height)
    
    img.composite(fg_img, 0, 0)
        
    return img