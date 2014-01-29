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

import motor

from tornado import web, websocket, ioloop, gen
from tornado.options import define, options

from pynbome import pynbome, image

import utils
import database
from config import SETTINGS

define("port", default=8000, help="run on the given port", type=int)


class UploadHandler(web.RequestHandler):
    """Upload image file from computer or URL"""
    
    def post(self):
        # Upload from computer
        if self.request.files:
            fileinfo = self.request.files['file'][0]
            fname = fileinfo['filename']
            ext = os.path.splitext(fname)[1] # file extension
        
            cname = str(uuid.uuid4()) + ext
        
            image_file = fileinfo['body']
        
        # Upload from URL
        else:
            # self.get_argument() doesn't work here, 
            # because Angular returns json.
            # So try to manually parse request body
            body = json.loads(self.request.body)
            
            if 'url' in body:
                # Retrieve image file from specified urllib
                
                image_file = urllib.urlopen(body['url']).read()
                ext = urllib.unquote(body['url']).decode('utf-8').split('.')[-1]
                cname = str(uuid.uuid4()) + '.' + ext
            else:
                data = {'error': 'No URL'}
                self.finish(data)
            
        full_image_path = os.path.join(SETTINGS['upload_tmp'], cname)
            
        with open(full_image_path, 'w') as f:
            f.write(image_file)
            
        # Create pynbome image object
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
    """Apply patterns and filters and preview edited image"""
    
    def post(self):
        body = json.loads(self.request.body)
        
        original_image_path = os.path.join(SETTINGS['upload_tmp'], body['original'])
        preview_image_path = os.path.join(SETTINGS['upload_tmp'], body['preview'])
        
        os.remove(preview_image_path)
        
        img = image.Image(filename=original_image_path)
        
        # Apply patterns if necessary
        if body['filters'] and body['combine']:
            img.combine()
        
        # Apply selected filters
        for filter_name in body['filters']:
            img.psychedelic(filter_name)
        
        # Save image preview
        preview_cname = str(uuid.uuid4()) + '.jpg'
        img.save(os.path.join(SETTINGS['upload_tmp'], preview_cname))
        
        data = {'original': body['original'], 'preview': preview_cname}
        
        self.finish(data)

  
class SaveHandler(web.RequestHandler):
    """Save image when editing was done"""
    
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
        
        # Create cropped and resized thumbnail
        img.image.crop(width/2-120, height/2-120, width=width/3, height=width/3)
        img.resize(120)
        
        img.save(small_image_path)
        
        new_image = {
            'src': image_name,
            'date': utils.from_unix(image_name[:-4]),
            'unixtime': float(image_name[:-4]),
            'ip': utils.get_ip(self.request),
            'likes': database.images['likes']
        }
        
        # Inserting item into db
        self.insert(new_image.copy())
        
        data = {'new_image': new_image}
        
        # Send new image data to websocket clients
        UpdatesHandler.send_updates(data)
        
        self.finish(data)
        
    def insert(self, item):
        db = SETTINGS['db']
        
        item.update(likes=database.images['likes'])
        
        db.images.insert(item, callback=database.insert_callback)


class GetLatestHandler(web.RequestHandler):
    """Get latest images, sort if necessary"""
    
    # Sort constants
    SORT_BY_DATE = 'new'
    SORT_BY_LIKES = 'best'
    SORT_CRITERIAS = (SORT_BY_DATE, SORT_BY_LIKES)
    
    @web.asynchronous
    def get(self):
        """
        GET request without params means that we need images
        sorted by date
        """
        
        self.sort_by = self.SORT_BY_DATE
        
        db = SETTINGS['db']
        
        fields = {'_id': False}
        
        # Select image items
        cursor = db.images.find(fields=fields).sort([('_id', -1)]).limit(36)
        cursor.to_list(callback=self.finish_callback)
        
    @web.asynchronous
    def post(self):
        """POST request's body must contain sort_by parameter"""
        
        body = json.loads(self.request.body)
        self.sort_by = body['sort_by']
        
        db = SETTINGS['db']
        
        fields = {'_id': False}
        
        if self.sort_by == self.SORT_BY_LIKES:
            # Sort by likes count
            
            sort_command = [('likes.count', -1), ('_id',  -1)]
        
            cursor = db.images.find(fields=fields).sort(sort_command).limit(36)
            cursor.to_list(callback=self.finish_callback)
    
    def finish_callback(self, result, error):
        """Finish data retrieving"""
        
        if error:
            raise error
        elif result:
            data = {
                'images': result, 
                'client_ip': utils.get_ip(self.request),
                'sort_by': self.sort_by,
                'sort_criterias': self.SORT_CRITERIAS
            }
            
            self.finish(data)
        else:
            # No data, trying to import existing files into database
            utils.import_files_to_mongo()


class GetFiltersHandler(web.RequestHandler):
    """Return list of pynbome filters"""
    
    def get(self):
        data = {'filters': pynbome.list_filters()}
        
        self.finish(data)


class LikeHandler(web.RequestHandler):
    """Like/unlike image handler"""
    
    @web.asynchronous
    @gen.engine # we'll use inline callbacks
    def post(self):
        db = SETTINGS['db']
      
        body = json.loads(self.request.body)
        
        item = body['image']
        ip = utils.get_ip(self.request)
        
        # Get item
        db_item = yield motor.Op(db.images.find_one, {'unixtime': item['unixtime']})
        
        _id = db_item['_id']
        
        # Save like/unlike on item
        if ip in db_item['likes']['data']:
            db_item['likes']['data'].remove(ip)
            db_item['likes']['count'] -= 1
        else:
            db_item['likes']['data'].append(ip)
            db_item['likes']['count'] += 1
        
        # Update item
        update_command = {'$set': {'likes': db_item['likes']}}
        yield motor.Op(db.images.update, {'_id': _id}, update_command)
        
        data = {'likes': db_item['likes']}
        
        self.finish(data)


class ImageHandler(web.RequestHandler):
    """Fetch one image info"""
  
    @web.asynchronous
    @gen.engine
    def get(self, unixtime):
        db = SETTINGS['db']
        
        db_item = yield motor.Op(db.images.find_one, {'unixtime': float(unixtime)})
        
        data = {
            'src': db_item['src'],
            'likes': db_item['likes'],
            'date': db_item['date'],
            'unixtime': db_item['unixtime']
        }
        
        self.finish(data)


class UpdatesHandler(websocket.WebSocketHandler):
    """Handler for send updates through websocket"""
    
    socket_clients = set()
    
    def open(self):
        self.socket_clients.add(self)
        
    def on_close(self):
        self.socket_clients.remove(self)
  
    @classmethod
    def send_updates(cls, data):
        for client in cls.socket_clients:
            client.write_message(data)


class MainHandler(web.RequestHandler):
    """Angular app's main page"""
    
    def get(self):
        # We don't use render() because angular templates
        # and tornado templates are not friends
        with open('public/index.html') as f:
            self.write(f.read())


application = web.Application([
    (r'/api/upload', UploadHandler),
    (r'/api/preview', PreviewHandler),
    (r'/api/save', SaveHandler),
    (r'/api/get_latest', GetLatestHandler),
    (r'/api/get_filters', GetFiltersHandler),
    (r'/api/like', LikeHandler),
    (r'/api/image/(\d+\.\d+)', ImageHandler),
    (r'/updates', UpdatesHandler),
    (r'/', MainHandler),
    (r'/image/\d+.\d+', MainHandler),
    (r'/(.*)', web.StaticFileHandler, {"path": "public"})
    ],
    **SETTINGS
)


if __name__ == "__main__":
    options.parse_command_line()
    application.listen(options.port)
    ioloop.IOLoop.instance().start()
