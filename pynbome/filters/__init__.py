# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# pynbome library
# __init__.py (c) Mikhail Mezyakov <mihail265@gmail.com>
#
# I think, it's good place to put some decorators

import tempfile

def prepare_filter(apply_filter):
    """Generate temporary filenames and save image before processing"""
    
    def wrapper(*args, **kwargs):
        img = args[0]
        
        _, input_filename = tempfile.mkstemp(suffix='.png')
        _, output_filename = tempfile.mkstemp(suffix='.png')
        
        img.save(filename=input_filename)
        
        return apply_filter(input_filename, output_filename)
      
    return wrapper