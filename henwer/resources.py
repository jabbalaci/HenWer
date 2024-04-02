#!/usr/bin/env python
# -*- coding: utf-8 -*-
# contains some helper class

import configparser
import os
import traceback
import webbrowser

import wx.html

# these constants will be used in all modules
NO_MANGA_ERROR = "Devi prima scegliere un manga!"
ERROR_CAPTION = "ManWer | Errore"
ERROR_STYLE = wx.OK | wx.ICON_ERROR

"""The preferences file is formatted as following:
[name]
option1: value

[name2]
option1: value
option2: value"""


def write_preferences(section, items, filename="preferences"):
    conf = configparser.ConfigParser()
    conf.read(filename)
    if not conf.has_section(section):
        conf.add_section(section)
    fp = open(filename, "w")
    if isinstance(items, dict):
        items = tuple(items.items())
    else:
        items = tuple(items)
    for v, k in items:
        conf.set(section, v, k)

    conf.write(fp)
    fp.close()


def get_preferences(section, filename="preferences"):
    # let's create a ConfigParser object
    conf = configparser.ConfigParser()
    conf.read(filename)
    try:
        val = dict((v, eval(k)) for v, k in conf.items(section))
    except configparser.NoSectionError:
        val = {}
    finally:
        return val


def log_error(filename="error_log.txt"):
    """Simple function, logs an error in a file"""
    f = open(filename, "a")
    traceback.print_exc(file=f)
    f.write("\n\n")
    f.close()


# messagedialog: a simple message dialog, with a htmlwindow and two buttons
# NOTE: links will opens in the default browser
class HtmlMessageDialog(wx.Dialog):
    def __init__(self, parent, title, file, size=(350, 500)):
        wx.Dialog.__init__(self, parent, -1, title)
        sizer = wx.FlexGridSizer(2, 1, 0, 0)
        self.message_html = wx.html.HtmlWindow(self, -1, size=size)
        self.ok_button = wx.Button(self, 0, "&Close")
        sizer.Add(self.message_html, flag=wx.EXPAND | wx.ALL | wx.ALIGN_CENTRE_HORIZONTAL, border=6)
        sizer.Add(self.ok_button, flag=wx.ALIGN_CENTRE_HORIZONTAL | wx.ALL, border=6)

        self.message_html.LoadFile(file)

        # set the sizer
        self.SetSizer(sizer)
        sizer.AddGrowableRow(0, 1)
        sizer.Fit(self)

        # events bindings
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(wx.EVT_BUTTON, self.on_close, id=0)
        self.Bind(wx.html.EVT_HTML_LINK_CLICKED, self.link_clicked, id=-1)

    def on_close(self, event):
        self.Destroy()

    def link_clicked(self, event):
        # overload this event, so the link will open in the browser, depending
        # on the webbrowser module
        webbrowser.open(event.GetLinkInfo().GetHref())


class CreateZipDialog(wx.Dialog):
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, -1, title)
        sizer = wx.FlexGridSizer(2, 3, 0, 0)
        dir_label = wx.StaticText(self, -1, "Cartella:")
        name_label = wx.StaticText(self, -1, "Nome:")

        self.dir_text = wx.TextCtrl(self, -1, size=(250, -1))
        self.name_text = wx.TextCtrl(self, -1)

        browse_button = wx.Button(self, 0, "Sfoglia")
        ok_button = wx.Button(self, wx.ID_OK, "Ok")

        self.auto_naming_box = wx.CheckBox(self, 2, "Nomina automaticamente il file")

        sizer.Add(dir_label, 1, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, border=3)
        sizer.Add(self.dir_text, 1, wx.ALL | wx.EXPAND, border=3)
        sizer.Add(browse_button, 1, wx.ALL | wx.EXPAND, border=3)

        sizer.Add(name_label, 1, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, border=3)
        sizer.Add(self.name_text, 1, wx.ALL | wx.EXPAND, border=3)
        sizer.AddSpacer(1)

        sizer.AddSpacer(1)
        sizer.Add(self.auto_naming_box, 1, wx.ALL | wx.EXPAND, border=3)
        sizer.Add(ok_button, 1, wx.ALL | wx.EXPAND, border=3)

        self.SetSizer(sizer)
        sizer.AddGrowableCol(1, 0)
        w, h = sizer.GetMinSize()
        self.SetSize((w, h + 35))

        self.Bind(wx.EVT_BUTTON, self.on_browse, id=0)
        self.Bind(wx.EVT_BUTTON, self.on_ok, id=wx.ID_OK)
        self.Bind(wx.EVT_CHECKBOX, self.on_checkbox, id=2)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.GetParent().save_in_zip = 0
        self.path = ""

    def on_checkbox(self, event):
        if self.auto_naming_box.GetValue():
            self.name_text.SetEditable(False)
            self.name_text.SetBackgroundColour(wx.Colour(236, 233, 216))
            self.name_text.SetValue("")
            self.name_text.Refresh()
        else:
            self.name_text.SetBackgroundColour(wx.NullColour)
            self.name_text.Refresh()
            self.name_text.SetEditable(True)

    def on_browse(self, event):
        dird = wx.DirDialog(self, "Scegli dove salvare lo zip")
        if dird.ShowModal() == wx.ID_OK:
            self.path = dird.GetPath()
            self.dir_text.SetValue(self.path.replace(os.path.expanduser("~"), "~"))

    def on_ok(self, event):
        name = self.name_text.GetValue()
        path = os.path.expanduser(self.dir_text.GetValue())
        if not (path or self.auto_naming_box.GetValue()):
            wx.MessageDialog(
                self, "Devi specificare entrambi i campi!", ERROR_CAPTION, style=ERROR_STYLE
            ).ShowModal()
            return
        if not os.path.exists(path):
            wx.MessageDialog(
                self, "La cartella specificata non esiste.", ERROR_CAPTION, style=ERROR_STYLE
            ).ShowModal()
            return
        if os.path.splitext(name)[1].lower() != ".zip":
            name += ".zip"
            self.name_text.SetValue(name)
        if name in os.listdir(path):
            wx.MessageDialog(
                self,
                "%s esiste gi�. Specifica un altro nome." % name,
                ERROR_CAPTION,
                style=ERROR_STYLE,
            ).ShowModal()
            return
        if self.auto_naming_box.IsChecked():
            name = ""
        self.path = os.path.join(path, name)
        self.GetParent().save = 2
        self.on_close(event)

    def on_close(self, event):
        self.GetParent().zip_path = self.path
        self.Destroy()


class MyToolBar(wx.ToolBar):
    def __init__(self, parent, *args, **kwargs):
        wx.ToolBar.__init__(self, parent, *args, **kwargs)

    def AddMany(self, elements):
        for t in elements:
            if t == "sep":
                self.AddSeparator()
            else:
                id, tooltip, img = t
                self.AddTool(id, tooltip, img)
