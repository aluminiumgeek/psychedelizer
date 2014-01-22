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
import shutil
from datetime import datetime

from tornado import web, websocket, ioloop
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
    @web.asynchronous
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
                cname = str(uuid.uuid4()) + '.' + ext
            else:
                data = {'error': 'No URL'}
                self.finish(data)
            
        full_image_path = os.path.join(SETTINGS['upload_tmp'], cname)
            
        with open(full_image_path, 'w') as f:
            f.write(image_file)
            
        img = image.Image(filename=full_image_path)
        
        width, height = img.size()
        if width > 600:
            img.resize(width=600)
        elif height > 600:
            img.resize(height=600)
        
        preview_cname = str(uuid.uuid4()) + '.jpg'
        img.save(os.path.join(SETTINGS['upload_tmp'], preview_cname))
        
        shutil.copy2(
            os.path.join(SETTINGS['upload_tmp'], preview_cname),
            os.path.join(SETTINGS['upload_tmp'], cname)
        )

        data = {'original': cname, 'preview': preview_cname}

        self.finish(data)

class PreviewHandler(web.RequestHandler):
    @web.asynchronous
    def post(self):
        body = json.loads(self.request.body)
        
        original_image_path = os.path.join(SETTINGS['upload_tmp'], body['original'])
        preview_image_path = os.path.join(SETTINGS['upload_tmp'], body['preview'])
        
        os.remove(preview_image_path)
        
        img = image.Image(filename=original_image_path)
        if body['filters'] and body['combine']:
            img.combine()
        
        for filter_name in body['filters']:
            img.psychedelic(filter_name)
        
        preview_cname = str(uuid.uuid4()) + '.jpg'
        img.save(os.path.join(SETTINGS['upload_tmp'], preview_cname))
        
        data = {'original': body['original'], 'preview': preview_cname}
        
        self.finish(data)
  
class SaveHandler(web.RequestHandler):
    @web.asynchronous
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
        
        width, height = img.size()
        
        img.image.crop(width/2-120, height/2-120, width=width/3, height=width/3)
        img.resize(120)
        
        img.save(small_image_path)
        
        data = {'new_image': image_name}
        
        UpdatesHandler.send_updates(data)
        
        self.finish(data)

class GetLatestHandler(web.RequestHandler):
    def get(self):
        images = self.get_images()
        
        data = {'images': images[::-1][:8]}
        
        self.finish(data)
      
    def get_images(self):
        content_directory = SETTINGS['saved_files']
        images = [image for image in os.listdir(content_directory)]
        images = filter(lambda x: not x.startswith('s') and not x.startswith('.'), images)
        images.sort(key=lambda x: float(x[:-4])) # sort by unixtime
        
        return [{'src': image, 'date': utils.from_unix(image[:-4])} for image in images]

class GetFiltersHandler(web.RequestHandler):
    def get(self):
        data = {'filters': pynbome.list_filters()}
        
        self.finish(data)

class LikeHandler(web.RequestHandler):
    pass


socket_clients = set()
class UpdatesHandler(websocket.WebSocketHandler):
    def open(self):
        socket_clients.add(self)
        
    def on_close(self):
        socket_clients.remove(self)
  
    @staticmethod
    def send_updates(data):
        for client in socket_clients:
            client.write_message(data)


application = web.Application([
    (r'/api/upload', UploadHandler),
    (r'/api/preview', PreviewHandler),
    (r'/api/save', SaveHandler),
    (r'/api/get_latest', GetLatestHandler),
    (r'/api/get_filters', GetFiltersHandler),
    (r'/api/like', LikeHandler),
    (r'/updates', UpdatesHandler),
    (r'/(.*)', web.StaticFileHandler, {"path": "public"})
    ],
    **SETTINGS
)


if __name__ == "__main__":
    options.parse_command_line()
    application.listen(options.port)
    ioloop.IOLoop.instance().start()