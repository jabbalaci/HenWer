#!/usr/bin/env python

import time

import wx


class Gauge(wx.Frame):
    def __init__(self, parent, id, title, capacity):
        wx.Frame.__init__(self, parent, id, title, size=(300, 160))

        self.count = 0
        self.capacity = capacity

        panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)

        self.gauge = wx.Gauge(panel, -1, capacity, size=(250, 25))
        # to correctly show the text in the center without stripping its right side
        tmp_size = len(str(self.capacity)) * 2 + len(" of ")
        self.text = wx.StaticText(panel, -1, "_" * tmp_size)
        self.btn1 = wx.Button(panel, wx.ID_CLOSE)

        self.Bind(wx.EVT_BUTTON, self.close, self.btn1)

        hbox1.Add(self.gauge, 1, wx.ALIGN_CENTRE)
        hbox2.Add(self.text, 1)
        hbox3.Add(self.btn1, 1)

        vbox.Add((0, 20), 0)
        vbox.Add(hbox1, 0, wx.ALIGN_CENTRE)
        vbox.Add((0, 30), 0)
        vbox.Add(hbox2, 1, wx.ALIGN_CENTRE)
        vbox.Add(hbox3, 1, wx.ALIGN_CENTRE)

        panel.SetSizer(vbox)
        self.Centre()
        self.btn1.Disable()
        self.Show(True)

    def close(self, event):
        self.Destroy()

    def set_value(self, value):
        self.count = value
        if self.count >= self.capacity:
            self.btn1.Enable()
            self.btn1.SetFocus()
        self.gauge.SetValue(value)
        self.text.SetLabel("%d of %d" % (self.count, self.capacity))
        self.update()

    def update(self):
        self.Update()


# eof class Gauge

if __name__ == "__main__":
    app = wx.App()
    li = range(15)
    g = Gauge(None, -1, "Downloading Images", len(li))
    for e in li:
        g.set_value(e + 1)
        time.sleep(0.1)
    app.MainLoop()
