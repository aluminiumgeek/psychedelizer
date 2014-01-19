#!/usr/bin/env python

import random
import subprocess
import tempfile

from wand.image import Image

def apply_filter(img):
    _, input_filename = tempfile.mkstemp(suffix='.png')
    _, output_filename = tempfile.mkstemp(suffix='.png')
    
    width, height = img.size
    img.crop(width=width, height=width)
    
    img.save(filename=input_filename)
    
    
    
    command = './lib/pseudocolor -o {2} {0} {1}'.format(
        input_filename,
        output_filename,
        random.randint(70, 190)
    )
    
    process = subprocess.Popen(command.split())
    process.wait()
    
    return Image(filename=output_filename)