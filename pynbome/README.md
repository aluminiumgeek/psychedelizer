pynbome
=============

A Python library to make psychedelic images

##Requirements##
* [Wand](http://wand-py.org/)

##Filters##
There're several psychedelic filters:

* **color** - rainbow colored transformation

* **disperse** - dispersion effect

* **glass** - view through tiled glass
* **kaleidoscope** - kaleidoscope effect

* **lsd** - combine source image lsd pattern

* **nbome** - combine source image nbome pattern

Filter sources located inside <code>filters</code> directory

##Usage##
###Basic usage###
```python
from pynbome.image import Image

img = Image(filename='test.jpg')
img.combine()
img.psychedelic()

img.save('test.png')
```

###List combine's patterns for image###
Image.combine() method takes pattern image name as first argument. If pattern was not specified, a random pattern applies

```python
patterns = img.list_patterns()

pattern_name = patterns[0]
img.combine(pattern_name)
```

###List image filters###
Image.psychedelic() method takes filter name as first argument. If filter was not specified, a random filter applies

```python
filters = img.list_filters()

filter_name = filters[0]
img.psychedelic(filter_name)
```

###Using several transformation###
Of course you can apply patterns and filters several times

```python
from pynbome.image import Image

img = Image(filename='test.jpg')

for i in range(3):
    img.combine()
    img.psychedelic()

img.save('test.png')
```

###Image state###
There's history of applied patterns and filters in Image object

```python
for i in range(3):
    img.combine()
    img.psychedelic()

print img.state
```
