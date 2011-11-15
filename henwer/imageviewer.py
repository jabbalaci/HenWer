#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import os
import imghdr
import resources
import imageinfo
import goto
from cStringIO import StringIO
import Image # PIL.Image Module
import random
from clipboard import text_to_clipboards


def bmp_to_pil(image):
    pil = Image.new('RGB', (image.GetWidth(), image.GetHeight()))
    pil.fromstring(image.GetData())
    return pil
    
def pil_to_image(pil):
    image = wx.EmptyImage(pil.size[0], pil.size[1])
    image.SetData(pil.convert('RGB').tostring())
    return image

class FileDragDrop(wx.FileDropTarget):
    def __init__(self, win):
        wx.FileDropTarget.__init__(self)
        self.win = win
    
    def OnDropFiles(self, x, y, filenames):
        list = []
        self.win.GetParent().local_file = 1
        for file in filenames:
            if os.path.isdir(file):
                list.extend(map(lambda p: os.path.join(file, p), os.listdir(file)))
            else:
                list.append(file)
        list = filter(lambda p: os.path.isfile(p) and imghdr.what(p), list)
        self.win.GetParent().filelist.extend(list)


class ImageWindow(wx.ScrolledWindow):
    def __init__(self, parent):
        #print sys._getframe().f_code.co_name
        wx.ScrolledWindow.__init__(self, parent, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        self.parent = parent
        self.image = None
        self.or_image = None
        self.to_zoom = 0
        self.must_zoom = 0
        self.show_text = 0
        self.hide_cursor = resources.get_preferences("Schermo intero").get("hide cursor", False)
        
        self.timer = wx.Timer(self, -1)
        
        fdd = FileDragDrop(self)
        self.SetDropTarget(fdd)

        self.SetBackgroundColour(self.GetParent().backcolour)
        #self.SetBackgroundColour(wx.Color(144,238,144))

        self.Bind(wx.EVT_PAINT, self.on_paint)
        #self.SetScrollbars(5, 5, 0, 0)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_KEY_DOWN, self.key_down)
        self.Bind(wx.EVT_TIMER, self.hide_mouse_cursor)
        self.Bind(wx.EVT_MOTION, self.mouse_move)
        #self.Bind(wx.EVT_MOUSEWHEEL, self.on_mousewheel)
        #self.Bind(wx.EVT_RIGHT_DOWN, self.onRightDown)
    
    #def onRightDown(self, event):
    #    #print "rightdown"
    #    conMenu = wx.Menu()
    #    zoom = wx.MenuItem(conMenu, 0, "Zoom")
    #    conMenu.AppendItem(zoom)
    #    self.PopupMenu(conMenu)
    
    def clear_dc(self):
        self.image = None
        dc = wx.ClientDC(self)
        dc.Clear()
        #self.SetBackgroundColour(self.GetParent().backcolour)
    
    def mouse_move(self, event):
        #print sys._getframe().f_code.co_name
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        if self.hide_cursor and self.GetParent().IsFullScreen():
            wx.CallAfter(self.timer.Start, 2000)
    
    def hide_mouse_cursor(self, event):
        #print sys._getframe().f_code.co_name
        self.SetCursor(wx.StockCursor(wx.CURSOR_BLANK))

    def zoom_in(self, event):
        #print sys._getframe().f_code.co_name
        self.must_zoom = 1
        self.to_zoom += 10
        text = self.parent.GetStatusBar().GetStatusText(3).split('@')[0].strip()
        if self.to_zoom > 400:
            self.to_zoom = 400
        self.parent.SetStatusText("%s @ %s %%" % (text, self.to_zoom), 3)
        self.zoom(self.to_zoom)
    
    def zoom_out(self, event):
        #print sys._getframe().f_code.co_name
        self.must_zoom = 1
        self.to_zoom -= 10
        text = self.parent.GetStatusBar().GetStatusText(3).split('@')[0].strip()
        if self.to_zoom < 10:
            self.to_zoom = 10
        self.parent.SetStatusText("%s @ %s %%" % (text, self.to_zoom), 3)
        self.zoom(self.to_zoom)
        
    def zoom_100(self, event):
        #print sys._getframe().f_code.co_name
        self.must_zoom = 1
        self.to_zoom = 100
        text = self.parent.GetStatusBar().GetStatusText(3).split('@')[0].strip()
        self.parent.SetStatusText("%s @ %s %%" % (text, self.to_zoom), 3)
        self.zoom(self.to_zoom)
        
    def zoom_fit(self, event):
        self.fit_window(event)
        self.zoom(self.to_zoom)
    
    def key_down(self, event):
        #print sys._getframe().f_code.co_name
        # see http://www.wxpython.org/docs/api/wx.KeyEvent-class.html for key codes
        key = event.GetKeyCode()
        key_func = { ord('F'):               self.zoom_fit,
                     ord('+'):               self.zoom_in,
                     ord('-'):               self.zoom_out,
                     ord(']'):               self.zoom_in,                     
                     ord('['):               self.zoom_out,
                     ord('='):               self.zoom_100,
                     ord('H'):               self.parent.show_key_bindings,
                     ord('M'):               self.parent.toggle_maximize,
                     ord('I'):               self.show_image_info,
                     ord('G'):               self.show_goto_img,
                     ord('R'):               self.goto_random_img,
                     ord('Y'):               self.copy_abs_path,
                     ord('S'):               self.toggle_to_save,
                     ord('D'):               self.toggle_to_delete,
                     ord('W'):               self.toggle_to_wallpaper,
                     ord('C'):               self.parent.commit_changes,
                     ord('A'):               self.mark_all_to_be_saved,                     
                     wx.WXK_F11:             self.toggle_fullscreen,
                     wx.WXK_NUMPAD_ADD:      self.zoom_in, #+ on the numpad
                     wx.WXK_NUMPAD_SUBTRACT: self.zoom_out #- on the numpad
                   }
        if self.image is not None:
            if key in [wx.WXK_LEFT, wx.WXK_PAGEUP, wx.WXK_UP]:
                self.parent.on_previous(event)
            if key in [wx.WXK_RIGHT, wx.WXK_PAGEDOWN, wx.WXK_DOWN]:
                self.parent.on_next(event)
        if key in key_func:
            key_func[key](event)
        else:
            event.Skip()
        #self.Refresh()
    
    def change_colour(self, colour):
        self.SetBackgroundColour(colour)
        self.Refresh()
    
    def toggle_fullscreen(self, event):
        #print sys._getframe().f_code.co_name
        parent = self.GetParent()
        if parent.IsFullScreen():
            parent.ShowFullScreen(False)
        else:
            parent.ShowFullScreen(True)
            if self.hide_cursor:
                self.timer.Start(2000, True)

    def change_image(self, image):
        #print "change_image"
        #print sys._getframe().f_code.co_name
        if isinstance(image, wx.Image):
            self.image = image
        else:
            self.image = wx.ImageFromStream(StringIO(image))
        self.or_image = self.image
        self.must_zoom = 0
        self.SetScrollbars(5, 5, 0, 0)
        self.Refresh(False)
        
#    def print_status(self, event):
#        if self.image is None:
#            return
#        #print sys._getframe().f_code.co_name
#        #show help. Only in fullscreen mode
#        dc = wx.ClientDC(self)
#        self.DoPrepareDC(dc)
#        if not self.show_text:
#            dc.SetTextForeground(wx.GREEN)
#            dc.SetFont(wx.Font(20,  wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
#            for n, line in enumerate( ["Jabba", "Laci"] ):
#                dc.DrawText(line, 20, 20 + n*30)
#        else:
#            dc.Clear()
#            #self.Refresh()
#        
#        self.show_text = not self.show_text

    def copy_abs_path(self, event):
        if self.image is None:
            return
        #print sys._getframe().f_code.co_name
        #show help. Only in fullscreen mode
        img = self.parent.filelist[self.parent.n]
        self.parent.SetStatusText(img.path, 0)
        text_to_clipboards(img.path)
        
    def toggle_to_save(self, event):
        if self.image is None:
            return
        # else
        img = self.parent.filelist[self.parent.n]
        if img.local_file:
            str = "You're browsing a local folder, it makes no sense to save it."
            dial = wx.MessageDialog(None, str, 'Exclamation', wx.OK | wx.ICON_EXCLAMATION)
            dial.ShowModal()
            return
        # else
        img.to_save = not img.to_save
        self.parent.set_status_text()
        self.parent.set_commit()
        self.parent.set_osd_text()
        
    def toggle_to_delete(self, event):
        if self.image is None:
            return
        # else
        img = self.parent.filelist[self.parent.n]
        if not img.local_file:
            str = "You cannot delete an online image."
            dial = wx.MessageDialog(None, str, 'Exclamation', wx.OK | wx.ICON_EXCLAMATION)
            dial.ShowModal()
            return
        # else
        img.to_delete = not img.to_delete
        self.parent.set_status_text()
        self.parent.set_commit()
        self.parent.set_osd_text()
        
    def toggle_to_wallpaper(self, event):
        if self.image is None:
            return
        # else
        img = self.parent.filelist[self.parent.n]
        img.to_wallpaper = not img.to_wallpaper
        self.parent.set_status_text()
        self.parent.set_commit()
        self.parent.set_osd_text()
    
    def on_size(self, event):
        #print sys._getframe().f_code.co_name
        if self.image:
            self.Refresh()
        self.parent.on_size()
    
    def on_paint(self, event):
        w, h = self.GetSizeTuple()
        #print sys._getframe().f_code.co_name
        if self.image is not None:
            dc = wx.PaintDC(self)
            self.DoPrepareDC(dc)
            dc.Clear()
            if not self.must_zoom:
                self.fit_window(event)
            #if the width (or height) of the image is bigger than the size of the window, offX (or offY) is 0
            self.offX = max(w/2 - self.image.GetWidth() / 2, 0)
            self.offY = max(h/2 - self.image.GetHeight() / 2, 0)
            dc.DrawBitmap(self.image.ConvertToBitmap(), self.offX, self.offY)
        else:
            event.Skip()

    def fit_window(self, event):
        """scale the image so it can fit the screen, leaving about a 2% margin top and bottom"""
        self.image = self.or_image
        #print sys._getframe().f_code.co_name
        w, h = self.GetSizeTuple()
        hi = h - (5*h)/100
        iW = self.image.GetWidth()
        iH = self.image.GetHeight()
        nw = hi*iW/iH
        nh = hi
        if nh < iH or nw < iW:
            self.image = pil_to_image(bmp_to_pil(self.image).resize((nw, nh), Image.BILINEAR))
            #self.image = self.image.Scale(nw, nh)
        else:
            nw = iW
            nh = iH
        self.img_size_percent = 100*nh/iH
        self.to_zoom = self.img_size_percent
        text = self.parent.GetStatusBar().GetStatusText(3).split('@')[0].strip()
        self.parent.SetStatusText("%s @ %s %%" %(text, self.img_size_percent), 3)
        
    def show_image_info(self, event):
        if self.image is not None:
            imageinfo.ImageInfo(self, -1, 'Image Info', self.parent)
            
    def show_goto_img(self, event):
        if len(self.parent.filelist) == 0:
            return
        # else
        self.from_goto = -1
        goto.GotoBox(self, -1, '', self.parent.n + 1, len(self.parent.filelist))
        # OK, self.from_goto is set from GotoBox
        if self.from_goto == -1:
            return
        # else
        self.parent.n = self.from_goto-1-1   # -1 because of 0-based index, -1 to step on the previous image
        self.parent.on_next(event)           # step forward to the specified image
        
    def goto_random_img(self, event):
        nb_imgs = len(self.parent.filelist)   # number of images 
        if  nb_imgs in [0, 1]:
            return
        # else
        jump_to = random.randrange(1, nb_imgs+1)   # interval [1, nb_imgs]
        self.parent.n = jump_to-1-1   # -1 because of 0-based index, -1 to step on the previous image
        self.parent.on_next(event)    # step forward to the specified image
        
    def mark_all_to_be_saved(self, event):
        if len(self.parent.filelist) == 0:
            return
        # else
        dial = wx.MessageDialog(None, 'Do you want to mark all images to be saved?', 'Question', 
            wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
        answer = dial.ShowModal()
        if answer == wx.ID_NO:
            return
        # else
        for img in self.parent.filelist:
            img.to_save = True
        self.parent.set_status_text()
        self.parent.set_commit()
        self.parent.set_osd_text()
    
    def zoom(self, percent, quality="BILINEAR"):
        #print sys._getframe().f_code.co_name
        if self.image:
            self.image = self.or_image
            w = self.image.GetWidth()
            h = self.image.GetHeight()
            nw = percent*w/100
            nh = h*nw/w
            #if not USE_PIL:
            #    self.image = self.image.Scale(nw, nh)
            #else: #the PIL is installed, so we use it
            self.image = pil_to_image(bmp_to_pil(self.image).resize((nw, nh), getattr(Image, quality)))
            self.img_size_percent = percent
            self.SetScrollbars(10, 10, nw/10+1, nh/10+1)
            self.Refresh(False)
        else:
            wx.MessageDialog(self, "Seleziona un'immagine prima", resources.ERROR_CAPTION, style=resources.ERROR_STYLE).ShowModal()
