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

def get_ip(request):
    """Return ip from HTTP headers. If it's empty, return remote_ip from request instance"""

    if 'X-Real-Ip' in request.headers:
        return request.headers['X-Real-Ip']
    else:
        return request.remote_ip

def import_files_to_mongo():
    """Import unindexed files to the database"""
    
    import os
    from tornado import gen, ioloop
    from config import SETTINGS
    
    @gen.engine
    def do_insert(items):
        for item in items:
            arguments = yield gen.Task(db.images.insert, item)
            result, error = arguments.args
            
            if error:
                raise error
        
        ioloop.IOLoop.instance().stop()
    
    images = os.listdir(SETTINGS['saved_files'])
    images = filter(lambda x: not x.startswith('s') and not x.startswith('.'), images)
    images.sort(key=lambda x: float(x[:-4]))
    
    images_items = (
        {
            'src': image, 
            'date': from_unix(image[:-4]),
            'unixtime': float(image[:-4]),
            'ip': '',
            'likes': []
        }
        for image in images
    )
    
    db = SETTINGS['db']
    do_insert(images_items)
    ioloop.IOLoop.instance().start()
    
