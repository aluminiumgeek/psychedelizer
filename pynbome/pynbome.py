# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# pynbome library
# pynbome.py (c) Mikhail Mezyakov <mihail265@gmail.com>
#
# Psychedelic image processing
#
# pip install Wand

import os
import pkgutil

DATA_DIR = 'data'

def list_filters():
    """Return list of filters"""
    
    modules_iter = pkgutil.iter_modules([os.path.join(os.path.dirname(__file__), 'filters')])
    return [name for _, name, _ in modules_iter]
      
def list_patterns():
    """Return list of patterns"""
    
    return os.listdir(os.path.join(os.path.dirname(__file__), DATA_DIR))
