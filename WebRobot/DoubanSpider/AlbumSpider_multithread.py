# -*- coding:utf-8 -*-
"""
Spider for DouBan album, the multi-thread version.
It is more efficient than the previous version.
"""
import urllib
import urllib2
import re
import threading
import time


class DBS():
    def __init__(self):
        self.count = 0
        self.fPhotourl = ''

    def getPage(self, in_url):
        url = in_url
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().decode('utf-8')

    def getAlbum(self, url):
        photo_url = url
        self.getPhoto(photo_url)

    def getPhoto(self, photoUrl):
        self.count += 1
        if self.count <= 10:
            self.openPhoto(photoUrl)
        else:
            print "The program is done"
            self.count = 0
            pass


    def openPhoto(self, photoUrl):
        page = self.getPage(photoUrl)
        pattern = re.compile('<img src="(.*)\.jpg" />')
        item = re.findall(pattern, page)
        imgurl = item[0] + '.jpg'
        print 'Get image:', imgurl
        self.saveImg(imgurl)
        pattern = re.compile('<link rel="next" href="(.*?)"/>')
        item = re.findall(pattern, page)
        print 'Get next', item[0]
        self.getPhoto(item[0])


    def saveImg(self, imgUrl):
        u = urllib.urlopen(imgUrl)
        img = u.read()
        pattern = re.compile('http://.*?/public/(.*)')
        item = re.findall(pattern, imgUrl)
        f = open(item[0], 'wb')
        f.write(img)
        f.close()


def main():
    alcont = DBS()
    threads = []
    nloops = [0:3]
    url = ['url1',
           'url2',
           'url3',
           'url4']
    for i in nloops:
        thread = threading.Thread(target=alcont.getAlbum(url[i]))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    startime = time.clock()
    main()
    endtime = time.clock()
    print (endtime - startime)