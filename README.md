psychedelizer
=============

Web application and library (pynbome) that makes your pictures a little psychedelic.  
Production version runs on http://psychedelizer.0x80.ru

## Requirements
* [ImageMagick](http://imagemagick.org/)
* [Wand](http://wand-py.org/)
* [Tornado](http://tornadoweb.org)
* [MongoDB](http://www.mongodb.org)
* [Motor](http://motor.readthedocs.org/en/stable/)

## Web application
Backend was written in Python using Tornado framework and MongoDB. Backend provides RESTful API for the frontend that built on AngularJS.

## Library
Pynbome library also written in Python and uses ImageMagick through Wand interface for image processing.
