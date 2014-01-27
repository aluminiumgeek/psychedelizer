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

from wand.image import Image
from . import prepare_filter

@prepare_filter
def apply_filter(input_filename, output_filename):
    settings = {
        'spread': random.randint(2, 6),
        'density': random.randint(5, 10),
        'curviness': random.randint(4, 9)
    }
    
    script_path = os.path.join(os.path.dirname(__file__), '../lib/disperse')
    command = '{0} -s {3} -d {4} -c {5} {1} {2}'.format(
        script_path,
        input_filename,
        output_filename,
        settings['spread'],
        settings['density'],
        settings['curviness']
    )
    
    process = subprocess.Popen(command.split())
    process.wait()
    
    return Image(filename=output_filename), settings
