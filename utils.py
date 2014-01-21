# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# psychedelizer.0x80.ru
# utils.py (c) Mikhail Mezyakov <mihail265@gmail.com>
#
# Some utils

from datetime import datetime

def from_unix(unixtime):
    return datetime.fromtimestamp(float(unixtime)).strftime('%Y-%m-%d %H:%M:%S')
