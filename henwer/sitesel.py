#!/usr/bin/env python

import os
import threading

import wx

func = ['gather_gallery_list', 'get_referer', 'get_relative_save_dir']

def get_manga(classname):
    return classname.manga
   
def get_choice(dir):
    l = [el for el in os.listdir(dir) if os.path.splitext(el)[1] == '.py']
    return [os.path.splitext(el)[0] for el in l if el != "__init__.py"]
    
class SiteSelector(wx.Dialog):
    def __init__(self, parent, title):
        #print sys._getframe().f_code.co_name
        wx.Dialog.__init__(self, parent, -1, title, style=wx.DEFAULT_DIALOG_STYLE)
        self.jobID = 0
        sizer = wx.GridBagSizer(2, 2)
        self.manga = None
        self.urls = []
        
        self.parent = parent

        t1 = wx.StaticText(self, -1, "Select a site: ")
        self.site_combo = wx.ComboBox(self, 0, choices=get_choice('./backend'), style=wx.CB_READONLY)
        
        t2 = wx.StaticText(self, -1, "Select a gallery: ")
        self.manga_combo = wx.ComboBox(self, 1)
        
        ok_button = wx.Button(self, 3, 'OK')
        canc_button = wx.Button(self, 4, 'Cancel')
        
        sizer.Add(t1, (1, 0), flag=wx.ALIGN_CENTRE_VERTICAL|wx.ALL, border=5)
        sizer.Add(self.site_combo, (1, 1), (1, 4), flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=5)
        sizer.Add(t2, (2, 0), flag=wx.ALIGN_CENTRE_VERTICAL|wx.ALL, border=5)
        sizer.Add(self.manga_combo, (2, 1), (1, 4), flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=5)
        sizer.Add(ok_button, (4, 0), flag=wx.ALIGN_CENTRE_VERTICAL|wx.ALL, border=5)
        sizer.Add(canc_button, (4, 1), (1, 2), flag=wx.TOP|wx.BOTTOM, border=5)

        self.SetSizer(sizer)
        
        self.Bind(wx.EVT_COMBOBOX, self.select_site, id=0)
        self.Bind(wx.EVT_COMBOBOX, self.select_manga, id=1)
        self.Bind(wx.EVT_BUTTON, self.on_ok, id=3)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, id=4)
        
        w, h = sizer.CalcMin()
        self.SetClientSize((w+10, h))

    def on_ok(self, event):
        #print sys._getframe().f_code.co_name
        #url = self.manga.site + self.url[self.chap_combo.GetSelection()]
        #self.parent.site = url
        self.parent.site = self.urls[self.manga_combo.GetSelection()]
        # to know where to save the file
        self.parent.save_dir_relative = self.manga.get_relative_save_dir(self.site_combo.GetValue(), self.manga_combo.GetValue())
        self.parent.referer = self.manga.get_referer()
        self.Destroy()
    
    def on_cancel(self, event):
        self.Destroy()
    
    def select_site(self, event):
        s = self.site_combo.GetValue()
        self.manga = __import__('backend.' + s, fromlist=func)
        self.manga_combo.Clear()
        #self.chap_combo.Clear()
        threading.Thread(target=self.append_item).start()
    
    def select_manga(self, event):
        #print sys._getframe().f_code.co_name
        #self.chap_combo.Clear()
        #threading.Thread(target=self.get_chaps).start()
        #print ">>> ", self.urls[self.manga_combo.GetSelection()]
        pass
    
    def append_item(self):
        #print sys._getframe().f_code.co_name
        self.SetCursor(wx.StockCursor(wx.CURSOR_WAIT))
        self.site_combo.Enable(False)
        self.manga_combo.SetValue("Loading galleries...")
        self.site = self.site_combo.GetValue()
        n, self.urls = self.manga.gather_gallery_list()
        for el in n:
            self.manga_combo.Append(str(el))
        self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        self.site_combo.Enable(True)
