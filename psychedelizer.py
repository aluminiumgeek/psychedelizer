# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# psychedelizer.0x80.ru
# psychedelizer.py (c) Mikhail Mezyakov <mihail265@gmail.com>
#

import os
import time
import uuid
import urllib
import json
from datetime import datetime

import tornado.ioloop
from tornado import web
from tornado.options import define, options

from pynbome import pynbome, image

import utils

define("port", default=8000, help="run on the given port", type=int)

SETTINGS = {
    'upload_tmp': 'public/tmp',
    'saved_files': 'public/content',
    'debug': True
}

class UploadHandler(web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        if self.request.files:
            fileinfo = self.request.files['file'][0]
            fname = fileinfo['filename']
            ext = os.path.splitext(fname)[1]
        
            cname = str(uuid.uuid4()) + ext
        
            image_file = fileinfo['body']
        else:
            # self.get_arument() doesn't work here, 
            # because Angular returns json.
            # So trying to manually parse request body
            body = json.loads(self.request.body)
            if 'url' in body:
                image_file = urllib.urlopen(body['url']).read()
                ext = urllib.unquote(body['url']).decode('utf-8').split('.')[-1]
                cname = str(uuid.uuid4()) + ext
            else:
                data = {'error': 'No URL'}
                self.finish(data)
            
        full_image_path = os.path.join(SETTINGS['upload_tmp'], cname)
            
        with open(full_image_path, 'w') as f:
            f.write(image_file)
            
        img = image.Image(filename=full_image_path)
        #img.combine()
        preview_cname = str(uuid.uuid4()) + '.jpg'
        img.save(os.path.join(SETTINGS['upload_tmp'], preview_cname))

        data = {'original': cname, 'preview': preview_cname}

        self.finish(data)

class PreviewHandler(web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        body = json.loads(self.request.body)
        
        original_image_path = os.path.join(SETTINGS['upload_tmp'], body['original'])
        preview_image_path = os.path.join(SETTINGS['upload_tmp'], body['preview'])
        
        os.remove(preview_image_path)
        
        img = image.Image(filename=original_image_path)
        if body['filters']:
            img.combine()
        
        for filter_name in body['filters']:
            img.psychedelic(filter_name)
        
        preview_cname = str(uuid.uuid4()) + '.jpg'
        img.save(os.path.join(SETTINGS['upload_tmp'], preview_cname))
        
        data = {'original': body['original'], 'preview': preview_cname}
        
        self.finish(data)
  
class SaveHandler(web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        body = json.loads(self.request.body)

        ext = body['image'].split('.')[-1]
        
        tmp_image_path = os.path.join(SETTINGS['upload_tmp'], body['image'])
        
        image_name = '{0}.{1}'.format(time.time(), ext)
        image_path = os.path.join(SETTINGS['saved_files'], image_name)
        
        small_image_path = os.path.join(
            SETTINGS['saved_files'], 
            's' + image_name
        )
        
        os.rename(tmp_image_path, image_path)
        
        img = image.Image(filename=image_path)
        img.resize(200)
        img.save(small_image_path)
        
        data = {'new_image': image_name}
        
        self.finish(data)

class GetLatestHandler(web.RequestHandler):
    def get(self):
        images = self.get_images()
        
        data = {'images': images}
        
        self.finish(data)
      
    def get_images(self):
        content_directory = SETTINGS['saved_files']
        images = [image for image in os.listdir(content_directory)]
        images = filter(lambda x: not x.startswith('s'), images)
        
        return [{'src': image, 'date': utils.from_unix(image[:-4])} for image in images]

class GetFiltersHandler(web.RequestHandler):
    def get(self):
        data = {'filters': pynbome.list_filters()}
        
        self.finish(data)

class LikeHandler(web.RequestHandler):
    pass


application = web.Application([
    (r'/api/upload', UploadHandler),
    (r'/api/preview', PreviewHandler),
    (r'/api/save', SaveHandler),
    (r'/api/get_latest', GetLatestHandler),
    (r'/api/get_filters', GetFiltersHandler),
    (r'/api/like', LikeHandler),
    (r'/(.*)', web.StaticFileHandler, {"path": "public"})
    ],
    **SETTINGS
)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()