# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# pynbome library
# image.py (c) Mikhail Mezyakov <mihail265@gmail.com>
#
# Pynbome image class

import os
import sys
import random
import importlib

from wand.image import Image as Wand

import pynbome

sys.path.append(os.path.dirname(__file__)) 

class NoImage(Exception):
    """Raises when no image specified for an instance of Image class"""
    
    def __str__(self):
        return 'No suitiable image or filename were specified'
      
class NoFilter(Exception):
    """Raises when no filter specified or filter doesn't exist"""
    
    def __str__(self):
        return 'No filter for image processing'


class Image(object):
    """Pynbome Image object"""
    
    STATE_PATTERNS = 'patterns'
    STATE_FILTERS = 'filters'
    
    def __init__(self, img=None, filename=None):
        """
        Constructor takes Wand image object or 
        creates image object from given filename.
        
        @param img: image object
        @type img: Wand Image
        
        @param filename: image path/filename
        @param filename: string
        """
        
        self.img = img if img is not None else Wand(filename=filename)
        
        if not self.img:
            raise NoImage
          
        self.state = {
            self.STATE_PATTERNS: [],
            self.STATE_FILTERS: []
        }
        
    @property
    def image(self):
        """Image object as is"""
        
        return self.img

    def get_state(self):
        """Get information about applied patterns and filters"""
        
        return self.state
      
    def save_state(self, state_type, state_value):
        """
        Save applied pattern or filter into image state.
        
        @param state_type: type of the applied thing (pattern or filter)
        @type state_type: string
        
        @param state_value: name of pattern or filter
        @type state_value: string
        """
        
        assert state_type in self.state, 'No such state type'
        
        self.state[state_type].append(state_value)
      
    def size(self):
        """
        Get image dimensions.
        
        @return: tuple contains width and height
        @rtype: tuple
        """
        
        return self.img.size
        
    def resize(self, width=None, height=None):
        """
        Resize image. Takes width and height as params. 
        If one of sides was not specified, it will 
        calculate proportionally to the other side.
        
        @param width: resize width
        @type width: int
        
        @param width: resize height
        @type width: int
        """
        
        assert not (width is None and height is None), 'No sizes specified'
        
        orig_w, orig_h = self.size()
        
        if width is None:
            width = height * orig_w / orig_h
        elif height is None:
            height = width * orig_h / orig_w
        
        self.img.resize(width, height)

    def combine(self, pattern_name=None):
        """
        Apply pattern to the image. A random one
        chooses, if no pattern specified.
        
        @param pattern_name: name of pattern to apply
        @type pattern_name: string
        """
        
        if pattern_name is None:
            pattern_name = random.choice(pynbome.list_patterns())
        
        pattern_filename = os.path.join(os.path.dirname(__file__), pynbome.DATA_DIR, pattern_name)
            
        with Wand(filename=pattern_filename) as fg_img:
            #width, height = fg_img.size
            #self.img.crop(width=width, height=height)
            img_w, img_h = self.size()
            
            fg_img.resize(img_w, img_h)
    
            self.img.composite(fg_img, 0, 0)
            
            self.save_state(self.STATE_PATTERNS, pattern_name)
        
    def psychedelic(self, filter_name=None, filter_module=None):
        """
        Apply selected filter to the image. A random one
        chooses, if no filter specified.
        
        @param filter_name: name of filter to apply
        @type filter_name: string
        
        @param filter_module: filter module
        @type filter_module: module
        """
        
        if filter_module is not None:
            image_filter = filter_module
        elif filter_name is not None:
            image_filter = self.get_filter(filter_name)
        else:
            image_filter = self.get_filter(random.choice(pynbome.list_filters()))
        
        self.img = image_filter.apply_filter(self.img)
        
        self.save_state(self.STATE_FILTERS, image_filter)
          
    def save(self, filename):
        """
        Save image to given filename.
        
        @param filename: a string contains path and image filename
        @type filename: string
        """
        
        self.img.save(filename=filename)
          
    def get_filter(self, filter_name):
        """
        Import and return filter by name
        
        @param filter_name: name of filter
        @type filter_name: string
        """
        
        return importlib.import_module('filters.%s'%filter_name)
