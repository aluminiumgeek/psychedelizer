# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# pynbome library
# kaleidoscope.py (c) Mikhail Mezyakov <mihail265@gmail.com>
#
# Kaleidoscope effect

import os
import random
import subprocess
import tempfile

from wand.image import Image

def apply_filter(img):
    _, input_filename = tempfile.mkstemp(suffix='.png')
    _, output_filename = tempfile.mkstemp(suffix='.png')
    
    #width, height = img.size
    #img.crop(width=width, height=width)
    
    img.save(filename=input_filename)
    
    orients = (0, 90, 180, 270)

    script_path = os.path.join(os.path.dirname(__file__), '../lib/kaleidoscopic')
    command = '{0} -m image -o {3} {4} {1} {2}'.format(
        script_path,
        input_filename,
        output_filename,
        random.choice(orients),
        random.choice(['-i', '']) # invert quadrant mask option
    )
    
    process = subprocess.Popen(command.split())
    process.wait()
    
    return Image(filename=output_filename)
