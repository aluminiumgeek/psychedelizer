pynbome
=============

A Python library to make psychedelic images

## Requirements
* [Wand](http://wand-py.org/)
* [ImageMagick](http://imagemagick.org/)

## Filters
There're several psychedelic filters:

* **color** - rainbow colored transformation

* **disperse** - dispersion effect

* **glass** - view through tiled glass

* **kaleidoscope** - kaleidoscope effect

Filter sources located inside <code>filters</code> directory

## Usage
### Basic usage
```python
from pynbome.image import Image

img = Image(filename='test.jpg')
img.combine()
img.psychedelic()

img.save('test.png')
```

### List image patterns
Image.combine() method takes pattern image name as first argument. If pattern was not specified, a random pattern applies

```python
from pynbome import pynbome

patterns = pynbome.list_patterns()

pattern_name = patterns[0]
img.combine(pattern_name)
```

### List image filters
Image.psychedelic() method takes filter name as first argument. If filter was not specified, a random filter applies

```python
from pynbome import pynbome

filters = pynbome.list_filters()

filter_name = filters[0]
img.psychedelic(filter_name)
```

### Use several transformations
Of course you can apply patterns and filters several times

```python
from pynbome.image import Image

img = Image(filename='test.jpg')

for i in range(3):
    img.combine()
    img.psychedelic()

img.save('test.png')
```

### Image state
There's history of applied patterns and filters in Image object

```python
for i in range(3):
    img.combine()
    img.psychedelic()

print img.state
```

## Gallery
![1](http://i.imgur.com/jdVT3kI.jpg)  
![2](http://i.imgur.com/fm3wTvV.jpg)  
![3](http://i.imgur.com/OPf42cu.jpg)  
![4](http://i.imgur.com/ifj27ev.jpg)
