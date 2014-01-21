# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# pynbome library
# color.py (c) Mikhail Mezyakov <mihail265@gmail.com>
#
# Rainbow colored transformation

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
    
    script_path = os.path.join(os.path.dirname(__file__), '../lib/pseudocolor')
    command = '{0} -o {3} {1} {2}'.format(
        script_path,
        input_filename,
        output_filename,
        random.randint(70, 190)
    )
    
    process = subprocess.Popen(command.split())
    process.wait()
    
    return Image(filename=output_filename)
