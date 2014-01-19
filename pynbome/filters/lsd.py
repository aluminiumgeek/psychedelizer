#!/usr/bin/env python

from wand.image import Image

def apply_filter(img):
  
    fg_filename = 'data/lsd.png'
    fg_img = Image(filename=fg_filename)
    
    width, height = fg_img.size
    img.resize(width)
    img.crop(width=width, height=height)
    
    img.composite(fg_img, 0, 0)
        
    return img