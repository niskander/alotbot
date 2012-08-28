# drawalot.py


"""A module for drawing alots using pictures from the internet
Required 3rd party libraries: 
    - flickrapi
    - python image manipulation (pythonware.com/library/pil)
    - Google-Search (https://github.com/BirdAPI/Google-Search-API)
"""

import Image
import ImageDraw
import ImageFont
import math
import flickrapi
import urllib
import webbrowser
import oauth2 as oauth
from google import *


COOKIECUTTER = 'alots/cookiecutter.png'
FLICKRFILE = 'flickraccount.txt' # contains apikey & apisecret
IMGURFILE = 'imguraccount.txt'
FONTFILE = 'interstate-black.ttf'
IMGUR_ACCESS = 'https://api.imgur.com/oauth/request_token'
IMGUR_REQUEST = 'https://api.imgur.com/oauth/authorize'
IMGUR_AUTHORIZE = 'https://api.imgur.com/oauth/access_token'
WIDTH = 0
HEIGHT = 1


class DrawAlot(object):
    def __init__(self, humanaid=True):
        self.cookiecutter = Image.open(COOKIECUTTER)
        self.alotwidth = self.cookiecutter.size[WIDTH]
        self.alotheight = self.cookiecutter.size[HEIGHT]

        # Flickr api (probably don't need this anymore)
        lines = open(FLICKRFILE).read().splitlines()
        self.flickrkey = lines[0]
        self.flickrsecret = lines[1]
        self.flickr = flickrapi.FlickrAPI(self.flickrkey, self.flickrsecret)

        # Imgur api
        line = open(IMGURFILE).read().splitlines()
        self.imgurkey = lines[0]
        self.imgursecret = lines[1]
        
        self.font = ImageFont.truetype(FONTFILE, 25)
        self.humanaid = humanaid

    def tileimage(self, tile, size):
        """Returns an image of size 'size' with a tiled background.
        The tile is the image 'tile'.
        """
        # x, y offsets because the alot cookiecutter will be masking
        # the top and top-left of the picture
        xoffset = 100
        yoffset = 120
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
        tile = self.gettile(thing)
        if tile is None: return None
        tiled = self.tileimage(tile, (self.alotwidth, self.alotheight))
        tiledalot = Image.composite(self.cookiecutter, tiled, mask=self.cookiecutter)
        painter = ImageDraw.Draw(tiledalot)
        painter.text((10, 10), 'AN ALOT OF %s' % thing.upper(), fill=(0, 0, 0), font=self.font)
        tiledalot.show()
        return tiledalot
    
    '''
    def getflickrimages(self, thing):
        """Returns an image of 'name' from the internet"""
        # all possible options:
        # http://www.flickr.com/services/api/flickr.photos.search.html
        options = {}
        options['query'] = thing
        options['sort'] = 'relevance'
        options['tags'] = thing
        #options['content_type'] = 1
        options['media'] = 'photos'
        options['extras'] = 'url_m'
        options['per_page'] = 40
        #options['is_getty'] = True
        results = self.flickr.photos_search(**options)
        if results.attrib['stat'] == 'ok':
            photos = results.find('photos').findall('photo')
            for photo in photos:
                webbrowser.open(photo.attrib['url_m'])
                answer = raw_input('Accept as image of %s? (\'y\', \'n\', or \'abort\') ' % name)
                # TODO: Find a way to automatically get good images
                # so that human inspection is not required
                # (I think adding 'picture of' to the query helps a bit)
                if answer == 'y':
                    tilesize = input('Enter the tile size: ')
                    imageurl = photo.attrib['url_m']
                    (filename, headers) = urllib.urlretrieve(imageurl)
                    tile = Image.open(filename)
                    tile = tile.resize(tilesize)
                    return tile
                elif answer == 'abort':
                    return None
        else:
            # TODO: raise FailedFetch
            pass
            return None
    '''
        
    def gettile(self, thing):
        options = ImageOptions()
        results = Google.search_images(thing, options)
        if self.humanaid:
            return self.getapprovedtile(results, thing)
        else:
            return self.urltoimage(results[0]['link'])

    def urltoimage(self, url):
        (filename, headers) = urllib.urlretrieve(url)
        image = Image.open(filename)
        return image

    def getapprovedtile(self, photos, thing):
        for photo in photos:
            url = photo.link
            webbrowser.open(url)
            answer = raw_input('Image of %s? (\'y\', \'n\', or \'abort\') ' % thing)
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
        

if __name__ == '__main__':
    d = DrawAlot()
    d.tiledalot('beer')

'''
    def tileimagelist(urls, size):
        """Returns an image of size 'size' of the images in the list 'urls'
        tiled.
        """
        tilesize = (100, 100)
        tiled = Image.new('RGBA', size, (255, 255, 255, 255))
        i = 0
        x = 0
        y = 0
        # TODO: This could iterate over the image several times, so save
        # all of them to disk first (or make sure that that doesn't happen)
        while i < len(urls):
            (filename, headers) = urllib.urlretrieve(urls[i].attrib['url_m'])
            tile = Image.open(filename)
            tile = tile.resize(tilesize)
            tiled.paste(tile, (x, y))
            i += 1
            if i >= len(urls): i = 0
            x += tilesize[WIDTH]
            if x >= size[WIDTH]:
                y += tilesize[HEIGHT]
                x = 0
                if y >= size[HEIGHT]: break
        #tiled.show()
        return tiled
'''
