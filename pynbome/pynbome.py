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
    return [name for _, name, _ in pkgutil.iter_modules(['filters'])]
      
def list_patterns():
    return os.listdir(DATA_DIR)