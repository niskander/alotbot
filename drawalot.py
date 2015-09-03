# drawalot.py


"""A module for drawing alots using pictures from the internet
Required 3rd party libraries: 
    - python image manipulation (pythonware.com/library/pil)
    - Google-Search (https://github.com/BirdAPI/Google-Search-API)
"""

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import math
import urllib
import webbrowser
import requesthandler
import os.path
import json
import pycurl
import StringIO
from base64 import b64encode
from google import *


COOKIECUTTER = 'alotbot/images/cookiecutter.png'
#FLICKRFILE = 'alotbot/flickraccount.txt' # contains apikey & apisecret
#IMGURFILE = 'alotbot/imguraccount.txt'
FONTFILE = 'alotbot/VeraBd.ttf'
IMGURUPLOAD = 'http://api.imgur.com/2/upload.json'
IMAGEDIR = 'alotbot/images/'
WIDTH = 0 # index
HEIGHT = 1 # index


class CurlBuffer:
   def __init__(self):
       self.contents = ''

   def body_callback(self, buf):
       self.contents = self.contents + buf


class DrawAlot(object):
    """A module for drawing alot of things"""
    def __init__(self, humanaid=True):
        self.cookiecutter = Image.open(COOKIECUTTER)
        self.alotwidth = self.cookiecutter.size[WIDTH]
        self.alotheight = self.cookiecutter.size[HEIGHT]
        
        # Flickr api (probably don't need this anymore)
        #lines = open(FLICKRFILE).read().splitlines()
        #self.flickrkey = lines[0]
        #self.flickrsecret = lines[1]
        #self.flickr = flickrapi.FlickrAPI(self.flickrkey, self.flickrsecret)
        ###

        # Imgur api
        #line = open(IMGURFILE).read().splitlines()
        #self.imgurkey = 'c515d926dddc9aa67cf84d13ed3e99d0'
        self.imgurkey = '0f327f3057bbbecb022a2169a4cc51da'
        self.font = ImageFont.truetype(FONTFILE, 25)
        self.humanaid = humanaid

    def tileimage(self, tile, size):
        """Returns an image of size 'size' with a tiled background.
        The tile is the image 'tile'.
        """
        print "Tile image..."
        # x, y offsets because the alot cookiecutter will be masking
        # the top and top-left of the picture
        xoffset = 50
        yoffset = 50
        tiled = Image.new('RGBA', size, (255, 255, 255, 255))
        rows = math.ceil(size[HEIGHT] / float(tile.size[HEIGHT]))
        cols = math.ceil(size[WIDTH] / float(tile.size[WIDTH]))
        for row in range(int(rows)):
            for col in range(int(cols)):
                x = col*tile.size[WIDTH] + xoffset
                y = row*tile.size[HEIGHT] + yoffset
                tiled.paste(tile, (x, y))
        return tiled

    def tiledalot(self, thing):
        """Returns an alot of thing"""
        print "tiledalot... Tile:"
        tile = self.gettile(thing)
        print tile
        if tile is None: return None
        tiled = self.tileimage(tile, (self.alotwidth, self.alotheight))
        tiledalot = Image.composite(self.cookiecutter,
                                    tiled,
                                    mask=self.cookiecutter)
        painter = ImageDraw.Draw(tiledalot)
        painter.text((10, 10),
                     'ALOT OF %s' % thing.upper(),
                     fill=(0, 0, 0), font=self.font)
        tiledalot.show()
        return tiledalot
        
    def gettile(self, thing):
        """Search google for a picture of 'thing' to use as a tile.
        Returns the an Image object."""
        
        print "gettile..."
        options = ImageOptions()
        results = Google.search_images(thing, options)
        print options
        print thing
        print "Results:"
        print results
        if self.humanaid:
            return self.getapprovedtile(results, thing)
        else:
            return self.urltoimage(results[0]['link'])

    def urltoimage(self, url):
        #print url
        (filename, headers) = urllib.urlretrieve(url)
        #print headers
        #print filename
        image = Image.open(filename)
        return image
        # TODO: This doesn't work with pictures from wikiepedia

    def getapprovedtile(self, photos, thing):
        """Go through the list of photos until one is approved by a human
        as being a picture of 'thing' or the operation is aborted.
        """
        for photo in photos:
            print "a photo..."
            #url = photo.link
            url = photo
            if 'wikimedia' in url.lower(): continue
            webbrowser.open(url)
            prompt = 'Image of %s? (\'y\', \'n\', or \'abort\') ' % thing
            answer = raw_input(prompt)
            # TODO: Find a way to automatically get good images
            if answer == 'y':
                tile = self.urltoimage(url)
                r = raw_input('Resize? (\'y\' or \'n\')')
                if r == 'y':
                    tilesize = input('Tile size: ')
                    tile = tile.resize(tilesize)
                return tile
            elif answer == 'abort':
                return None
                
    def uploadimage(self, filename):
        """Uploads the image at 'filename' to imgur and returns the url"""
        requesturl = IMGURUPLOAD
        data = {}
        data['key'] = self.imgurkey
        data['image'] = b64encode(open(filename, 'rb').read())
        '''
        response = requesthandler.reqhandler.postrequest(requesturl, data)
        s = response.read()
        print s
        js = json.loads(s)
        try:
            url = js['upload']['links']['original']
            print url
            return url
        except KeyError:
            # raise exception
            pass
        '''
        b = CurlBuffer()
        c = pycurl.Curl()
        values = [ \
          ("key", self.imgurkey), \
          ("image", data['image'])]
        c.setopt(c.URL, "http://api.imgur.com/2/upload.json")
        c.setopt(c.HTTPPOST, values)
        c.setopt(c.WRITEFUNCTION, b.body_callback)
        c.perform()
        c.close()
        print b.contents
        js = json.loads(b.contents)
        url = js['upload']['links']['original']
        # TODO: exception
        print url
        return url

    def drawandupload(self, thing):
        """Draws an alot of 'thing'; uploads to imgur; returns url"""
        filename = self.constructfilename(thing)
        if not os.path.isfile(filename):
            alot = self.tiledalot(thing)
            #alot = alot.resize((200, 150))
            alot.save(filename, 'png')
        url = self.uploadimage(filename)
        return url

    def constructfilename(self, thing):
        return IMAGEDIR + 'alotof' + thing + '.png'


if __name__ == '__main__':
    d = DrawAlot()
    d.drawandupload('fan')
