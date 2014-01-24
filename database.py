# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# psychedelizer.0x80.ru
# database.py (c) Mikhail Mezyakov <mihail265@gmail.com>
#
# Database schemes and callbacks

images = {
    'src': '',
    'date': '',
    'unixtime': float(),
    'ip': '',
    'likes': []
}

def insert_callback(result, error):
    if error:
        raise error
