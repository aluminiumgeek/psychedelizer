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

from wand.image import Image
from . import prepare_filter

@prepare_filter
def apply_filter(input_filename, output_filename):
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
