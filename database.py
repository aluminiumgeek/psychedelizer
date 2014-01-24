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
    'unixtime': 0.0,
    'ip': '',
    'likes': {
        'count': 0,
        'data': []
    }
}

def insert_callback(result, error):
    if error:
        raise error
