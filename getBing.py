#! /usr/bin/env python
# -*- coding:utf-8 -*-

from common import db
from common.helper import *
from common import config
import time
import os
import urllib
import urllib2
import re
import json
from datetime import datetime

import sys  
reload(sys)  
sys.setdefaultencoding('utf8') 

is_debug = False
def debug_output(info, debug = False):
    if (is_debug == True or debug == True):
        print "[" + str(time.strftime("%Y-%m-%d %H:%M:%S")) + "]"
        print info
        print "\r"


class getBing:
    def __init__(self, image_index=0):
        self.time = time.time()
        self.url  = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx='+str(image_index)+'&n=1&nc=1394591383800&pid=hp&FORM=HPENCN&video=0'
        self.img_path = '/tmp'
        self.root_path = os.getcwd()


    def getImgObj(self,url):
        #Host:cn.bing.com
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'}
        req    = urllib2.Request(url, headers=header)
        r      = urllib2.urlopen(req).read()
        r      = json.loads(r)
        
        try :
            r['images'][0]['url']
        except:
            return {};
        else:
            return r['images'][0]


    def getBingImg(self):
        img_obj = self.getImgObj(self.url)
        if (any(img_obj) == False):
            debug_output('no imgs', True)

        img_url  = img_obj['url'].replace('_1366x768', '1920x1080')
        img_name = datetime.now().strftime("%Y%m%d%H") + img_url[img_url.rindex("/")+1:]
        path     = self.img_path + "/" + img_name
        desc     = img_obj['copyright']
        old_url  = img_obj['urlbase']
        save_file_name = self.root_path + path
        
        if (img_url.find('http://cn.bing.com') == -1):
            img_url = 'http://cn.bing.com' + img_url;        

        r = urllib.urlretrieve(img_url, save_file_name)
        
        print save_file_name
        print "\r"

if __name__ == "__main__":
    #for i in range(0, 10):
    #    obj = getBing(i)
    #    obj.getBingImg();
    obj = getBing(0)
    obj.getBingImg();
