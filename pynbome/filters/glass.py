# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# pynbome library
# glass.py (c) Mikhail Mezyakov <mihail265@gmail.com>
#
# View through tiled glass

import os
import subprocess

from wand.image import Image
from . import prepare_filter

@prepare_filter
def apply_filter(input_filename, output_filename):
    settings = {
        'amount': 25,
        'granularity': 5
    }
    
    script_path = os.path.join(os.path.dirname(__file__), '../lib/glasseffects')    
    command = '{0} -e displace -a {3} -g {4} -w 0 -n 100 {1} {2}'.format(
        script_path,
        input_filename,
        output_filename,
        settings['amount'],
        settings['granularity']
    )
    
    process = subprocess.Popen(command.split())
    process.wait()
    
    return Image(filename=output_filename), settings
