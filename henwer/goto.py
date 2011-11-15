#!/usr/bin/env python

import wx

class GotoBox(wx.Dialog):
    def __init__(self, parent, id, title, curr, max):
        wx.Dialog.__init__(self, parent, id, title, size=(250, 180))

        self.box = None
        self.parent = parent

        wx.StaticBox(self, -1, ' Go to ', (5, 5), size=(240, 120))
        wx.StaticText(self, -1, 'Image', (60, 60))
        self.box = wx.SpinCtrl(self, -1, '1', (110, 55), (60, -1), min=1, max=max)
        self.box.SetValue(curr)
        wx.Button(self, 1, 'Ok', (90, 135), (60, -1))

        self.Bind(wx.EVT_BUTTON, self.OnClose, id=1)

        self.Centre()
        self.ShowModal()
        self.Destroy()

    def OnClose(self, event):
        if self.parent is not None:
            #print box.GetValue()
            self.parent.from_goto = self.box.GetValue() 
        self.Close()

if __name__ == "__main__":
    app = wx.App()
    GotoBox(None, -1, '', 5, 120)
    app.MainLoop()
