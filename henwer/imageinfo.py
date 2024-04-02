#!/usr/bin/env python

import myimage
import wx


class LeftPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id, style=wx.BORDER_SUNKEN)


class RightPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id, style=wx.BORDER_SUNKEN)


class ImageInfo(wx.Frame):
    def __init__(self, parent, id, title, manwer):
        self.manwer = manwer
        self.filelist = manwer.filelist
        self.pos = manwer.n
        self.width = 1024
        self.height = 480
        wx.Frame.__init__(self, parent, id, title, size=(self.width, self.height))

        self.mainPanel = wx.Panel(self, -1)
        self.leftPanel = LeftPanel(self.mainPanel, -1)
        self.rightPanel = RightPanel(self.mainPanel, -1)

        hbox = wx.BoxSizer()
        hbox.Add(self.leftPanel, 1, wx.EXPAND | wx.ALL, 5)
        hbox.Add(self.rightPanel, 1, wx.EXPAND | wx.ALL, 5)
        self.mainPanel.SetSizer(hbox)

        self.left_x = 10
        self.left_y = 10

        self.show_info()

        self.first_call = 1
        self.Bind(wx.EVT_KEY_DOWN, self.key_down)
        self.Bind(
            wx.EVT_KEY_UP, self.key_up
        )  # !!! Notice that it's wx.EVT_KEY_UP and not wx.EVT_KEY_DOWN

        self.mainPanel.SetFocus()

        self.Centre()
        self.Show(True)

    def show_info(self):
        self.add_line("local_file", str(self.manwer.local_file))
        self.add_line("path", self.filelist[self.pos].path)
        size = myimage.numberToPrettyString(self.filelist[self.pos].size)
        self.add_line("size", "%s (%s bytes)" % (self.filelist[self.pos].size_readable, size))
        if not self.manwer.local_file:
            self.add_line(
                "to_save",
                "%s (%d of %d marked to be saved)"
                % (
                    str(self.filelist[self.pos].to_save),
                    myimage.number_of_imgs_to_be_saved(self.filelist),
                    len(self.filelist),
                ),
            )
        if self.manwer.local_file:
            self.add_line(
                "to_delete",
                "%s (%d of %d marked to be deleted)"
                % (
                    str(self.filelist[self.pos].to_delete),
                    myimage.number_of_imgs_to_be_deleted(self.filelist),
                    len(self.filelist),
                ),
            )
        self.add_line(
            "to_wallpaper",
            "%s (%d of %d marked to be wallpapered)"
            % (
                str(self.filelist[self.pos].to_wallpaper),
                myimage.number_of_imgs_to_be_wallpapered(self.filelist),
                len(self.filelist),
            ),
        )

    def add_line(self, key, value):
        left = wx.TextCtrl(
            self.leftPanel,
            -1,
            size=(self.width / 2 - 30, 25),
            style=wx.TE_READONLY,
            pos=(self.left_x, self.left_y),
        )
        left.SetValue(key)
        right = wx.TextCtrl(
            self.rightPanel,
            -1,
            size=(self.width / 2 - 30, 25),
            style=wx.TE_READONLY,
            pos=(self.left_x, self.left_y),
        )
        right.SetValue(value)
        self.left_y += 30

    def OnOk(self, event):
        self.Close()

    def key_down(self, event):
        # print ">>> down"
        # see http://www.wxpython.org/docs/api/wx.KeyEvent-class.html for key codes
        if event.GetKeyCode() == ord("I"):
            self.OnOk(event)
        event.Skip()

    def key_up(self, event):
        if self.GetParent() and self.first_call:
            self.first_call = 0
            return
        # print ">>> up"
        # see http://www.wxpython.org/docs/api/wx.KeyEvent-class.html for key codes
        if event.GetKeyCode() == wx.WXK_ESCAPE or event.GetKeyCode() == ord("I"):
            self.OnOk(event)
        event.Skip()


if __name__ == "__main__":
    app = wx.App()
    ImageInfo(None, -1, "Image Info")
    app.MainLoop()
