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

from wand.image import Image
from . import prepare_filter

@prepare_filter
def apply_filter(input_filename, output_filename):
    orients = (0, 90, 180, 270)
    
    settings = {
       'orient': random.choice(orients),
       'invert': random.choice([True, False])
    }
    
    script_path = os.path.join(os.path.dirname(__file__), '../lib/kaleidoscopic')
    command = '{0} -m image -o {3} {4} {1} {2}'.format(
        script_path,
        input_filename,
        output_filename,
        settings['orient'],
        '-i' if settings['invert'] else '' # invert quadrant mask option
    )
    
    process = subprocess.Popen(command.split())
    process.wait()
    
    return Image(filename=output_filename), settings
