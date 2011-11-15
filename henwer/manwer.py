#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# I use the following naming convention:
# - joined_lower for method or function or variables
# - JOINED_UPPER for global constants, such as IDs
# - UpperCamelCase for class names

import os
import sys
import imghdr
import urllib, urllib2

#import threading

import wx

import sitesel
import resources
import imageviewer
#import optionsdialog as optdialog
import myimage
import screenscraper
import commit
import platform

#try:
#from cStringIO import StringIO as _SIO
#except ImportError:
#    from StringIO import StringIO as _SIO

__version__ = "0.1h"

ID_MENU_OPEN_URL = wx.NewId()
ID_MENU_OPEN_FILE = wx.NewId()

ID_QUIT = wx.NewId()

ID_OPEN_DIR = wx.NewId()
#
ID_COMMIT = wx.NewId()
#ID_OPEN_URL = wx.NewId()
ID_OPEN_URL_GALLERY = wx.NewId()
#
ID_PREVIOUS = wx.NewId()
ID_NEXT = wx.NewId()
ID_DOWN_ALL = wx.NewId()
ID_REMOVE_QUEUE = wx.NewId()

ID_SAVE_IN_DIR = wx.NewId()

ID_FIT_WINDOW = wx.NewId()
ID_ZOOM_DECREASE = wx.NewId() 
ID_ZOOM_INCREASE = wx.NewId()

ID_SHOW_SHORT = wx.NewId()
ID_ABOUT = wx.NewId()
ID_SWITCH_TO_LOCAL = wx.NewId()

NO_MANGA_ERROR = resources.NO_MANGA_ERROR
ERROR_CAPTION = resources.ERROR_CAPTION
ERROR_STYLE = resources.ERROR_STYLE

MAX = 15

class MyOpener(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'

#create an opener, so we can change its user-agent
urlopen = MyOpener().open
urlretrieve = MyOpener().retrieve

imgpath = lambda x: os.path.join("pixmaps", x)

class MReader(wx.Frame):
    def __init__(self, title, *args):
        #print sys._getframe().f_code.co_name
        #wx.Frame.__init__(self, None, -1, title, pos=(0, 0), size=wx.DisplaySize(), *args)
        wx.Frame.__init__(self, None, -1, title, pos=(0, 0), size=(1024, 768), *args)
        #self.name = ""
        self.where = "."
        self.site = ""   # will be modified by a site selector
        self.filelist = []
        self.completed = {}
        self.referer = None   # a referer for downloading images
        # where to save files, specified in the 'preferences' file
        self.save_dir = resources.get_preferences(platform.system()).get('save_dir', None)
        self.save_dir_relative = None   # it'll be set by SiteSelector
        if myimage.check_tmp_dir() == False:
            self.Destroy()
        if myimage.check_wallpapers_dir() == False:
            self.Destroy()
        self.check_save_dir(self.save_dir)
        #tbicon = wx.TaskBarIcon()
        
        icon = wx.Icon(imgpath("henwer_logo.ico"), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        if resources.get_preferences("Options").get("show_tray", False):
            self.tbicon = wx.TaskBarIcon()
            self.tbicon.SetIcon(icon, "HenWer %s - Running" %__version__)
        self.local_file = 0 # can have 2 values: 0 if the image is given over the internet
                            #                    1 for a local dir.
        self.n = -1
        self.backcolour = resources.get_preferences("Options").get('color', (0, 0, 0))
        self.dc = imageviewer.ImageWindow(self)
        self.img_zoom_percent = 0
        self.save = 1   #0 = do not save
                        #1 = Save in a dir (specified in self.where)
        self.manga = None #the module to use to download the images
        
        self.image = None #self.image is the image displayed in the ImageWindow
        #MENUBAR
        menubar = wx.MenuBar()
        self.menubar = menubar
        #FILE 
        file = wx.Menu()
        #FILE > OPEN
        open = wx.Menu()
        #FILE > OPEN > FROM URL
        from_url = wx.MenuItem(open, ID_MENU_OPEN_URL, "Da URL")
        open.AppendItem(from_url)
        #FILE > OPEN > FROM FILE
        from_dir = wx.MenuItem(open, ID_MENU_OPEN_FILE, "Da file locale")
        open.AppendItem(from_dir)
        
        #file.AppendMenu(0, "&Apri", open)
        #FILE > QUIT
        quit = wx.MenuItem(file, ID_QUIT, "&Quit")
        
        file.AppendItem(quit)
        #EDIT
        edit = wx.Menu()
        #EDIT > SAVE IN...
        save_in = wx.Menu()
        #EDIT > SAVE IN > DIR
        dir = wx.MenuItem(save_in, ID_SAVE_IN_DIR, "cartella", kind=wx.ITEM_RADIO)

        save_in.AppendItem(dir)
        
        #EDIT > ZOOM
        zoom = wx.Menu()
        #EDIT > ZOOM > FIT TO WINDOW SIZE
        fit_window = wx.MenuItem(zoom, ID_FIT_WINDOW, "Adatta a dimensioni")
        #EDIT > ZOOM > INCREASE
        increase_zoom = wx.MenuItem(zoom, ID_ZOOM_INCREASE, "Aumenta")
        decrease_zoom = wx.MenuItem(zoom, ID_ZOOM_DECREASE, "Diminuisci")

        zoom.AppendItem(increase_zoom)
        zoom.AppendItem(decrease_zoom)
        zoom.AppendItem(fit_window)

        edit.AppendMenu(3, "Zoom", zoom)
        edit.AppendMenu(4, "Salva in", save_in)
        
        #SETTINGS
        #settings = wx.Menu()
        #SETTINGS > OPTIONS
        #options = wx.MenuItem(settings, ID_OPTIONS, "Opzioni")
        
        #settings.AppendItem(options)
        
        #HELP
        help = wx.Menu()
        show_shortcut = wx.MenuItem(help, ID_SHOW_SHORT, "Show &Key Bindings")
        about = wx.MenuItem(help, ID_ABOUT, "&About")
        
        help.AppendItem(show_shortcut)
        help.AppendItem(about)
        
        #OPTIONS
        options = wx.Menu()
        switch_to_local = wx.MenuItem(help, ID_SWITCH_TO_LOCAL, "Switch to &local dir.")
        
        options.AppendItem(switch_to_local)
        
        #add the menu to the menubar
        menubar.Append(file, "&File")
        menubar.Append(options, "&Options")
        #menubar.Append(edit, "&Modifica")
        #menubar.Append(settings, "&Strumenti")
        menubar.Append(help, "&Help")
        self.SetMenuBar(menubar)
        #TOOLBAR
        self.toolbar = resources.MyToolBar(self, -1, style=wx.TB_TEXT|wx.TB_HORIZONTAL|wx.TB_FLAT)
        self.toolbar.AddMany([(ID_OPEN_DIR, "Open local", wx.Bitmap(imgpath("document-open.png"))),
                            #"sep",
                            (ID_OPEN_URL_GALLERY, "Open URL", wx.Bitmap(imgpath("folder-remote.png"))),
                            "sep",
                            (ID_COMMIT, "Commit", wx.Bitmap(imgpath("accept.png"))),
                            #(ID_OPEN_URL, "Apri (URL)", wx.Bitmap(imgpath("folder-remote.png"))),
                            "sep",
                            (ID_PREVIOUS, "Previous", wx.Bitmap(imgpath("go-previous.png"))),
                            (ID_NEXT, "Next", wx.Bitmap(imgpath("go-next.png"))),
                            "sep",
                            (ID_REMOVE_QUEUE, "Reset", wx.Bitmap(imgpath("process-stop.png")))])
        self.toolbar.Realize()
        self.SetToolBar(self.toolbar)
        self.toolbar.EnableTool(ID_PREVIOUS, False)
        self.toolbar.EnableTool(ID_NEXT, False)          
        self.toolbar.EnableTool(ID_REMOVE_QUEUE, False)
        self.toolbar.EnableTool(ID_COMMIT, False)

        #STATUSBAR
        self.statusbar = wx.StatusBar(self, -1)
        self.statusbar.SetFieldsCount(4)
        self.statusbar.SetStatusWidths(self.calculate_percent([30, 20, 30, 20]))
        self.SetStatusBar(self.statusbar)

        #BIND
        self.Bind(wx.EVT_MENU, self.open_from_url, id=ID_MENU_OPEN_URL)
        self.Bind(wx.EVT_MENU, self.open_from_local_file, id=ID_MENU_OPEN_FILE)

        self.Bind(wx.EVT_MENU, self.increase_zoom, id=ID_ZOOM_INCREASE)
        self.Bind(wx.EVT_MENU, self.decrease_zoom, id=ID_ZOOM_DECREASE)
        self.Bind(wx.EVT_MENU, self.fit_window_size, id=ID_FIT_WINDOW)
        
        self.Bind(wx.EVT_MENU, self.save_in_dir, id=ID_SAVE_IN_DIR)
        
        #self.Bind(wx.EVT_MENU, self.show_options, id=ID_OPTIONS)
        
        self.Bind(wx.EVT_MENU, self.show_key_bindings, id=ID_SHOW_SHORT)
        self.Bind(wx.EVT_MENU, self.show_about, id=ID_ABOUT)
        
        self.Bind(wx.EVT_MENU, self.switch_to_local_dir, id=ID_SWITCH_TO_LOCAL)

        self.Bind(wx.EVT_TOOL, self.open_dir, id=ID_OPEN_DIR)
        self.Bind(wx.EVT_TOOL, self.commit_changes, id=ID_COMMIT)
        #self.Bind(wx.EVT_TOOL, self.open_url, id=ID_OPEN_URL)
        self.Bind(wx.EVT_TOOL, self.open_url_gallery, id=ID_OPEN_URL_GALLERY)
        self.Bind(wx.EVT_TOOL, self.on_next, id=ID_NEXT)
        self.Bind(wx.EVT_TOOL, self.on_previous, id=ID_PREVIOUS)
        self.Bind(wx.EVT_TOOL, self.on_remove_queue, id=ID_REMOVE_QUEUE)
        #self.Bind(wx.EVT_TOOL, self.on_download_all, id=ID_DOWN_ALL)
        
        self.Bind(wx.EVT_MENU, self.on_close, id=ID_QUIT)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        
        self.enable_menu(1, 0, False)
        
        self.Centre()
        self.dc.SetFocus()   # to treat keyboard events

        if len(sys.argv) > 1:
            if os.path.isdir(sys.argv[1]):
                self.open_dir(None, dir_to_open=sys.argv[1])
            else:
                print '# error: {0} is not a valid directory.'.format(sys.argv[1])
    
    def toggle_maximize(self, event):
        self.Maximize(not self.IsMaximized()) 
    
    def on_remove_queue(self, event):
        self.n = -1
        self.filelist = []   # will be a list of MyImage objects
        self.dc.clear_dc()
        self.SetTitle('HenWer %s' % __version__)
        self.SetStatusText("", 0)
        self.SetStatusText("", 1)
        self.SetStatusText("", 2)
        self.toolbar.EnableTool(ID_PREVIOUS, False)
        self.toolbar.EnableTool(ID_NEXT, False)
        self.toolbar.EnableTool(ID_REMOVE_QUEUE, False)
        self.toolbar.EnableTool(ID_COMMIT, False)
        self.enable_menu(1, 0, False)
    
    def enable_menu(self, index, subindex, enable):
        menu = self.GetMenuBar()
        menu.GetMenu(index).FindItemByPosition(subindex).Enable(enable)
        
    def refresh(self):
        self.dc.change_colour(self.backcolour)
        
    def change_background_colour(self, colour):
        self.dc.SetBackgroundColour(colour)
        self.dc.Refresh()
        self.backcolour = colour
        
#    def show_options(self, event):
#        #let's show a little options dialog
#        optdialog.OptionDialog(self, "Manwer | Opzioni")
    
    def on_close(self, event):
        #print sys._getframe().f_code.co_name
        if self.confirm_commit(event) == wx.ID_YES:
            return
        # else
        self.Destroy()
    
    def save_in_dir(self, event):
        #print sys._getframe().f_code.co_name
        dird = wx.DirDialog(self, "Scegli dove salvare...")
        if dird.ShowModal() == wx.ID_OK:
            self.where = dird.GetPath()
            self.save = 1
    
    def show_about(self, event):
        #print sys._getframe().f_code.co_name
        about_dialog = resources.HtmlMessageDialog(self, "HenWer | About", "html/about.html",
                                                   size=(350, 320))
        about_dialog.Center()
        about_dialog.ShowModal()
        
    def switch_to_local_dir(self, event):
        dir_to_open = os.path.join(self.save_dir, self.save_dir_relative)
        self.on_remove_queue(event)
        self.open_dir(event, dir_to_open)
    
    def show_key_bindings(self, event):
        #print sys._getframe().f_code.co_name
        key_dialog = resources.HtmlMessageDialog(self, "HenWer | Key Bindings", "html/key_bindings.html",
                                                 size=(400, 600))
        key_dialog.Center()
        key_dialog.ShowModal()
        self.dc.SetFocus()   # give back the focus
    
    def fit_window_size(self, event):
        #print sys._getframe().f_code.co_name
        self.dc.fit_window(event)
        self.dc.Refresh()
    
    def open_from_url(self, event):
        #print sys._getframe().f_code.co_name
        self.open_url(event)
        
    def open_from_local_file(self, event):
        #print sys._getframe().f_code.co_name
        self.open_dir(event)

    def increase_zoom(self, event):
        #print sys._getframe().f_code.co_name
        try:
            self.dc.zoom_in()
            self.img_zoom_percent = self.dc.to_zoom
        except AttributeError:
            wx.MessageDialog(self, NO_MANGA_ERROR, ERROR_CAPTION, style=ERROR_STYLE).ShowModal()
    
    def decrease_zoom(self, event):
        #print sys._getframe().f_code.co_name
        try:
            self.dc.zoom_out()
            self.img_zoom_percent = self.dc.to_zoom
        except AttributeError:
            wx.MessageDialog(self, NO_MANGA_ERROR, ERROR_CAPTION, style=ERROR_STYLE).ShowModal()

    def confirm_commit(self, event):
        """We have made some changes that are not committed and
        we choose another action (open dir., close application)
        that might result in losing the changes. So notify the user."""
        if commit.there_is_something_to_commit(self):
            str = "You've made some changes.\nDo you want to commit them?"
            dial = wx.MessageDialog(None, str, 'Question', 
                                    wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
            if dial.ShowModal() == wx.ID_YES:
                self.commit_changes(event, confirmation = False)
                return wx.ID_YES
            else:
                return wx.ID_NO

    def open_dir(self, event, dir_to_open = None):
        if self.confirm_commit(event) == wx.ID_YES:
            return
        # else
        if dir_to_open is None:  
            dlg = wx.DirDialog(self, "Open local directory...", style=wx.DD_DEFAULT_STYLE)
            if dlg.ShowModal() == wx.ID_OK:
                self.local_file = 1
                path = dlg.GetPath()
            else:
                self.local_file = 0
            dlg.Destroy()
        else:
            self.local_file = 1
            path = dir_to_open
        #
        #
        if self.local_file == 1:    
            flist = [os.path.join(path, el) for el in os.listdir(path)
                            if os.path.isfile(os.path.join(path, el)) and
                            imghdr.what(os.path.join(path, el)) is not None]
            self.filelist = myimage.MyImageList(flist, self.local_file).get_list()
            #print self.filelist
            self.n = -1
            self.SetTitle('HenWer %s -- %s' % (__version__, path))
            if len(self.filelist) == 0:
                self.on_remove_queue(event)
            else:   # if there is at least 1 image available
                self.enable_menu(1, 0, False)   # switch to local: OFF
                self.toolbar.EnableTool(ID_REMOVE_QUEUE, True)
                # jump to the 1st image
                self.on_next(event)
        
#    def open_dir(self, event):  
#        dlg = wx.DirDialog(self, "Open local directory...", style=wx.DD_DEFAULT_STYLE)
#        if dlg.ShowModal() == wx.ID_OK:
#            self.local_file = 1
#            path = dlg.GetPath()
#            flist = [os.path.join(path, el) for el in os.listdir(path)
#                            if os.path.isfile(os.path.join(path, el)) and
#                            imghdr.what(os.path.join(path, el)) is not None]
#            self.filelist = myimage.MyImageList(flist, self.local_file).get_list()
#            #print self.filelist
#            self.n = -1
#            self.SetTitle('HenWer %s' % __version__)
#            if len(flist) == 0:
#                self.on_remove_queue(event)
#            else:   # if there is at least 1 image available
#                self.enable_menu(1, 0, False)   # switch to local: OFF
#                self.toolbar.EnableTool(ID_REMOVE_QUEUE, True)
#                #if len(self.filelist) > 0:   # jump to the 1st image
#                self.on_next(event)
#        else:
#            self.local_file = 0
#        dlg.Destroy()
            
    def open_url_gallery(self, event):
        if self.confirm_commit(event) == wx.ID_YES:
            return
        # else
        old_site = self.site
        a = sitesel.SiteSelector(self, 'Select backend')
        a.ShowModal()
        # self.site is set by the selector
        self.manga = sitesel.get_manga(a)
        new_site = self.site
        if (new_site == old_site or not new_site):
            return
        #
        self.local_file = 0
        flist = screenscraper.ExtractImageURLs().get_image_urls(self.site)
        self.filelist = myimage.MyImageList(flist, self.local_file).get_list()
        self.n = -1
        if len(flist) == 0:
            dial = wx.MessageDialog(None, 'No images could be extracted.\nThis gallery seems to be empty.', 
                                    'Exclamation', wx.OK | wx.ICON_EXCLAMATION)
            dial.ShowModal()
            self.on_remove_queue(event)
            return
        # else, if there is at least 1 image available
        self.enable_menu(1, 0, False)   # switch to local: OFF
        self.toolbar.EnableTool(ID_NEXT, True)
        self.toolbar.EnableTool(ID_REMOVE_QUEUE, True)
        self.SetTitle('HenWer %s -- %s' % (__version__, self.site))
        
        if len(self.filelist) > 0:   # jump to the 1st image
            self.on_next(event)
    
#    def open_url(self, event):
#        #print sys._getframe().f_code.co_name
#        self.enable_menu(1, 1, True)
#        a = sitesel.SiteSelector(self, 'Seleziona backend')
#        a.ShowModal()
#        self.manga = sitesel.get_manga(a)
#        self.completed = {}
#        try:
#            t = '@ ' + str(self.manga).split()[1].split('.')[-1].strip('\'')
#        except IndexError:
#            t = ""
#        else:
#            self.toolbar.EnableTool(ID_NEXT, True)
#            self.toolbar.EnableTool(ID_REMOVE_QUEUE, True)
#            self.SetTitle('HenWer %s %s'%(__version__, t))
#            self.local_file = 0
#            self.n = -1    

    def on_size(self):
        #print sys._getframe().f_code.co_name
        #when the frame inits it has no statusbar, but occours a on_size event, raising an exception
        try:
            self.statusbar.SetStatusWidths(self.calculate_percent([30, 20, 30, 20]))
        except AttributeError:
            pass
    
    def calculate_percent(self, percent):
        #print sys._getframe().f_code.co_name
        w = self.GetSizeTuple()[0]
        return [(i*w)/100 for i in percent]
    
    def on_download_all(self, event):
        #print sys._getframe().f_code.co_name
        self.toolbar.EnableTool(ID_DOWN_ALL, False)
        self.downloadAll()

    def on_next(self, event):
        if self.n == len(self.filelist) - 1:
            return
        # else
        #print sys._getframe().f_code.co_name
        self.SetCursor(wx.StockCursor(wx.CURSOR_WAIT))
        self.n += 1
        if self.n > 0:
            self.toolbar.EnableTool(ID_PREVIOUS, True)
        
        img = self.filelist[self.n]
        if not self.local_file:   # URL
            #self.toolbar.EnableTool(ID_NEXT, False)
            #threading.Thread(target=self.download).start()
            self.image = wx.Image(self.download_to_local(img))
        else: # images are in a local directory
            self.image = wx.Image(img.path)
        
        img.set_attributes()
        self.set_status_text()
        #self.SetStatusText("Image: %s/%s" % (self.n+1, len(self.filelist)), 1)
        self.paint()
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        self.set_arrows()
        self.set_osd_text()
        
    def download_to_local(self, img):
        if self.referer is None:
            urllib.urlretrieve(img.path, img.get_tmp_file_to_save_to())
        else:
            req = urllib2.Request(img.path)
            req.add_header('Referer', self.referer)
            response = urllib2.urlopen(req)
            
            output = open(img.get_tmp_file_to_save_to(), 'wb')
            output.write(response.read())
            output.close()
            
        return img.get_tmp_file_to_save_to()
        
    def set_arrows(self):        
        if self.n == 0:
            self.toolbar.EnableTool(ID_PREVIOUS, False)
        if self.n == len(self.filelist) - 1:
            self.toolbar.EnableTool(ID_NEXT, False)
            
    def set_commit(self):
        if commit.there_is_something_to_commit(self):
            self.toolbar.EnableTool(ID_COMMIT, True)
        else:
            self.toolbar.EnableTool(ID_COMMIT, False)

    def on_previous(self, event):
        if self.n == 0:
            return
        # else
        #print sys._getframe().f_code.co_name
        self.SetCursor(wx.StockCursor(wx.CURSOR_WAIT))
        self.n -= 1

        img = self.filelist[self.n]
        if not self.local_file:   # URL
            #self.toolbar.EnableTool(ID_PREVIOUS, False)
            #threading.Thread(target=self.download).start()
            self.image = wx.Image(self.download_to_local(img))
        else:   # local dir.
            self.image = wx.Image(img.path)

        img.set_attributes()
        self.set_status_text()
        #self.SetStatusText("Image: %s/%s" % (self.n+1, len(self.filelist)), 1)
        self.paint()
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        self.set_arrows()
        self.set_osd_text()
        
    def set_status_text(self):
        img = self.filelist[self.n]
        self.SetStatusText("Image: %s/%s" % (self.n+1, len(self.filelist)), 1)
        self.SetStatusText(img.file_name, 2)
        self.SetStatusText(img.get_status_text(short=False), 0)
#        if not self.local_file:
#            if img.to_save:   self.SetStatusText("save", 0)
#            else:                               self.SetStatusText("", 0)
#        else:   # if local file
#            if img.to_delete:   self.SetStatusText("delete", 0)
#            else:                                 self.SetStatusText("", 0)

    def set_osd_text(self):
        dc = wx.ClientDC(self.dc)
        self.dc.DoPrepareDC(dc)
        img = self.filelist[self.n]
        osd_text = img.get_status_text(short=True)
        if len(osd_text) > 0:
            dc.SetTextForeground(img.get_status_text_color())
            dc.SetFont(wx.Font(30,  wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
            for n, line in enumerate( osd_text.split() ):
                dc.DrawText(line, 20, 20 + n*40)
        else:
            self.dc.Refresh()

#    def download(self):
#        #print sys._getframe().f_code.co_name
#        self.url, path, name = self.manga.get_img_url(self.site, self.n)
#        self.statusbar.SetStatusText('Scaricando %s da %s...' % (name, self.site), 0)
#        img_path = os.path.join(self.where, path, name)
#        if img_path in self.completed:
#            self.image = wx.ImageFromStream(self.completed[img_path])
#        else:
#            page = urlopen(self.url)
#            meta = page.info()
#            data = page.read()
#            self.completed[img_path] = _SIO(data)
#            #print "size: %f kb" %(len(self.completed), self.n, float(meta.getheaders("Content-Length")[0]) / 1024)
#            if len(self.completed) >= MAX:
#                self.completed = {}
#            if self.save == 1: #in a dir
#                path = os.path.join(self.where, path)
#                if not os.path.exists(path):
#                    os.makedirs(path)
#                f = open(img_path, 'wb')
#                f.write(data)
##            if self.save == 2: #in a zip
##                if not os.path.splitext(self.zip_path)[1] == '.zip':
##                    self.zip_path += ' - '.join(path.split(os.sep)) + '.zip'
##                archive.save_file(self.zip_path, name, data)
#            #if save is 0 we already have the image in data stream.
#            self.image = wx.ImageFromStream(_SIO(data))
#        self.paint()
#        self.statusbar.SetStatusText('Fatto', 0)

    def check_save_dir(self, save_dir):
        problem = False
        if save_dir is None:
            str = "No save_dir is specified in your preferences, thus " + \
                  "you won't be able to save images."
            problem = True
        elif os.path.exists(save_dir) == False:
            str = "The save_dir directory specified in your preferences doesn't exist, thus " + \
                  "you won't be able to save images."
            problem = True
        elif os.path.isdir(save_dir) == False:
            str = "The save_dir directory specified in your preferences is not a directory, thus " + \
                  "you won't be able to save images."
            problem = True
        if problem:
            dial = wx.MessageDialog(None, str, 'Exclamation', wx.OK | wx.ICON_EXCLAMATION)
            dial.ShowModal()
            
    def commit_changes(self, event, confirmation = True):
        comm = commit.Commit(self, event)
        comm.start(confirmation)
        self.set_commit()
        self.set_osd_text()
    
    def paint(self):
        #print sys._getframe().f_code.co_name
        #self.dc = ImageWindow(self, wx.Image(self.path))
        img = self.image
        try:
            string = str(img.GetWidth()) + ', ' + str(img.GetHeight())
        except wx.PyAssertionError:
            return
        finally:
            self.toolbar.EnableTool(ID_NEXT, True)
            self.toolbar.EnableTool(ID_PREVIOUS, True)
        self.dc.change_image(img)
        self.statusbar.SetStatusText(string, 3)
        del img
