#!/usr/bin/env python

import os
from urlparse import urlparse
import resources
import wx
import platform
import time
from datetime import datetime

def number_of_imgs_to_be_saved(li):
    return len([e for e in li if e.to_save])

def number_of_imgs_to_be_deleted(li):
    return len([e for e in li if e.to_delete])

def number_of_imgs_to_be_wallpapered(li):
    return len([e for e in li if e.to_wallpaper])

class MyImageList:
    def __init__(self, imgList, local_file):
        self.li = []
        for im in imgList:
            self.li.append(MyImage(im, local_file))
        if local_file:
            import operator
            self.li.sort(key=operator.attrgetter('path'))
                
    def get_list(self):
        return self.li
    
# eof class MyImageList

class MyImage:
    tmp_dir = None   # will be set by check_tmp_dir()
    tmp_name = 'tmp-henwer'
    wallpapers_dir = None   # will be set by check_wallpapers_dir()
    
    def __init__(self, path, local_file):
        self.local_file = local_file
        self.path = path
        self.size = None
        self.size_readable = None
        self.to_save = False
        self.to_delete = False
        self.to_wallpaper = False
        if local_file:
            self.file_name = os.path.split(path)[1]
        else:
            self.file_name = os.path.split(urlparse(path)[2])[1]
        # debug
        self.file_ext = os.path.splitext(self.file_name)[1]
    
    def __str__(self):
        return self.file_name
    
    def __repr__(self):
        return self.__str__()
    
    def get_status_text(self, short):
        str = ""
        if self.local_file:
            if self.to_delete:
                if short:   str += "D"
                else:       str += "delete"
        else:   # if not a local file
            if self.to_save:
                if short:   str += "S"
                else:       str += "save"
        if self.to_wallpaper:
            if short:
                if len(str) > 0:
                    str += "\n"
                str += "W"
            else:       
                if len(str) > 0:
                    str += " + "
                str += "wallpaper"
        #    
        return str
    
    def get_status_text_color(self):
        color = None
        if self.to_wallpaper:
            color = wx.BLUE
        if self.to_save:
            color = wx.GREEN
        if self.to_delete:
            color = wx.RED
        #
        return color
    
    def set_attributes(self):
        if self.size is None:
            self.size =  os.path.getsize(self.get_local_path())
            self.size_readable = sizeof_fmt(self.size)
            
    def get_local_path(self):
        if self.local_file:
            return self.path
        else:
            #return MyImage.local_tmp_file
            return self.get_tmp_file_to_save_to()
        
    def get_tmp_file_to_save_to(self):
        return os.path.join(MyImage.tmp_dir, MyImage.tmp_name + self.file_ext)
    
# eof class MyImage

def sizeof_fmt(num):
    # tip from http://blogmag.net/blog/read/38/Print_human_readable_file_size
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def numberToPrettyString(n):
    """Converts a number to a nicely formatted string.
       Example: 6874 => '6,874'."""
    l = []
    for i, c in enumerate(str(n)[::-1]):
        if i%3==0 and i!=0:
            l += ','
        l += c
    return "".join(l[::-1])

def check_tmp_dir():
    tmp_dir = resources.get_preferences(platform.system()).get('tmp_dir', None)
    problem = False
    if tmp_dir is None:
        str = "No tmp_dir is specified in your preferences."
        problem = True
    elif os.path.exists(tmp_dir) == False:
        str = "The tmp_dir directory specified in your preferences doesn't exist."
        problem = True
    elif os.path.isdir(tmp_dir) == False:
        str = "The tmp_dir directory specified in your preferences is not a directory."
        problem = True
    if problem:
        dial = wx.MessageDialog(None, str, 'Error', wx.OK | wx.ICON_ERROR)
        dial.ShowModal()
        return False
    # else
    MyImage.tmp_dir = tmp_dir
    
def check_wallpapers_dir():
    wp_dir = resources.get_preferences(platform.system()).get('wallpapers_dir', None)
    problem = False
    if wp_dir is None:
        str = "No wallpapers_dir is specified in your preferences."
        problem = True
    elif os.path.exists(wp_dir) == False:
        str = "The wallpapers_dir directory specified in your preferences doesn't exist."
        problem = True
    elif os.path.isdir(wp_dir) == False:
        str = "The wallpapers_dir directory specified in your preferences is not a directory."
        problem = True
    if problem:
        dial = wx.MessageDialog(None, str, 'Error', wx.OK | wx.ICON_ERROR)
        dial.ShowModal()
        return False
    # else
    MyImage.wallpapers_dir = wp_dir
    
def get_timestamp():
    time.sleep(0.01)   # wait 10 msec. to guarantee unique timestamps
    lt = time.localtime(time.time())
    dt = datetime.now()
    return "%04d%02d%02d_%02d%02d%02d_%06.0f" % (lt[0], lt[1], lt[2], lt[3], lt[4], lt[5], dt.microsecond)

####################

if __name__ == "__main__":
    url = 'http://japancsaj.com/pic/rju_ri/rju_ri_9.jpg'
    fileName = os.path.split(urlparse(url)[2])[1]
    print fileName
    print "##########"
    for i in range(10):
        print get_timestamp()
