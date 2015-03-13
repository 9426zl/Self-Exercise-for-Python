# -*- coding:utf-8 -*-
import urllib
import urllib2
import cookielib
import re


class OPDouban:

    def __init__(self):
        self.loginUrl = 'http://www.douban.com/login'
        self.cookies = cookielib.CookieJar()
        self.postdata = urllib.urlencode({
            'source': 'index_nav',
            'form_email': '***@***.com',
            'form_password': '*******'
         })
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))

    def get_page(self):
        request = urllib2.Request(
            url=self.loginUrl,
            data=self.postdata)
        result = self.opener.open(request)
        print result.read()


opd = OPDouban()
opd.get_page()
