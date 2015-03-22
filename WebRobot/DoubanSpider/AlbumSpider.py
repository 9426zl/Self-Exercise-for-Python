# -*- coding:utf-8 -*-
"""
Web spider to collect the photo of designated douban
album, mode 1 for whole album, mode 2 for designated
start photo
"""
import urllib
import urllib2
import re


class AlbumSpider:
    def __init__(self):
        self.count = 0
        self.flag = ''


    def get_page(self, url):
        # acquire the designated url
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().decode('utf-8')


    def get_album(self, url, mode):
        # start the web spider by appointed mode
        if mode == 1:
            album_url = url
            page = self.get_page(album_url)
            pattern = re.compile('<div class="photo_wrap">.*?<a href="(.*?)" \
class="photolst_photo" title=".*?">.*?<img src=".*?" />', re.S)
            item = re.findall(pattern, page)
            photo_url = item[0]
        elif mode == 2:
            photo_url = url
        else:
            print "INVALID ENTRY"
            exit(1)

        self.get_photo(photo_url)


    def get_photo(self, photo_url):
        # decide whether the iteration should stop
        # by the flag
        if self.count == 0:
            self.flag = photo_url
        self.count += 1

        if (self.flag != photo_url) | (self.count == 1):
            self.open_photo(photo_url)
        else:
            return None


    def open_photo(self, photo_url):
        # open the photo and get url of next photo
        page = self.get_page(photo_url)

        pattern = re.compile('<img src="(.*)\.jpg" />')
        item = re.findall(pattern, page)
        img_url = item[0] + '.jpg'

        print 'Get image:', img_url
        self.save_img(img_url)

        pattern = re.compile('<link rel="next" href="(.*?)"/>')
        item = re.findall(pattern, page)

        print 'Get next', item[0]
        self.get_photo(item[0])


    def save_img(self, img_url):
        # save the designated photo
        u = urllib.urlopen(img_url)
        img = u.read()

        pattern = re.compile('http://.*?/public/(.*)')
        item = re.findall(pattern, img_url)

        f = open(item[0], 'wb')
        f.write(img)
        f.close()


if __name__ == '__main__':
    url = ''
    mode = '1'
    album = AlbumSpider()
    album.get_album(url, mode)