#!/usr/bin/env python

import unittest

from image import Image 

class PynbomeTest(unittest.TestCase):
    
    def setUp(self):
        self.image_filename = 'leary.jpg'
        self.image = open(self.image_filename)
        
        self.img = Image(filename=self.image_filename)
    
    def testResize(self):
        self.img.resize(100, 100)
        self.assertEqual( self.img.size(), (100,100) )
        
    def testFilterList(self):
        print 'Filters: {0}'.format(' '.join(self.img.list_filters()))
        
    def testPatternList(self):
        print 'Patterns: {0}'.format(' '.join(self.img.list_patterns()))
        
    def testCombine(self):
        self.img.combine()
        
        self.img.save('test.jpg')
        
        self.assertTrue(self.img.state[self.img.STATE_PATTERNS])
        
    def testPsychedelic(self):
        filter_name = self.img.list_filters()[0]
        self.img.psychedelic(filter_name='lsd')
        
        self.img.save('test.jpg')
        
        self.assertTrue(self.img.state[self.img.STATE_FILTERS])
        
    def testPsychedelize(self):
        self.img.combine()
        self.img.psychedelic()
        self.img.psychedelic()
        
        self.img.save('test.jpg')
        
        self.assertEqual(len(self.img.state[self.img.STATE_PATTERNS]), 1)
        self.assertEqual(len(self.img.state[self.img.STATE_FILTERS]), 2)


if __name__ == '__main__':
    unittest.main()