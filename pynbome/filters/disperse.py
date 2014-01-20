# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# pynbome library
# disperse.py (c) Mikhail Mezyakov <mihail265@gmail.com>
#
# Dispersion effect

import os
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
    
    
    s, d, c = random.randint(2, 6), random.randint(5, 10), random.randint(4, 9)
    script_path = os.path.join(os.path.dirname(__file__), '../lib/disperse')
    command = '{0} -s {3} -d {4} -c {5} {1} {2}'.format(
        script_path,
        input_filename,
        output_filename,
        s,
        d,
        c
    )
    
    process = subprocess.Popen(command.split())
    process.wait()
    
    return Image(filename=output_filename)
