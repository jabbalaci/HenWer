#!/usr/bin/env python

import wx
import myimage
import os
import download

def there_is_something_to_commit(manwer):
    delete = myimage.number_of_imgs_to_be_deleted(manwer.filelist) > 0
    save = myimage.number_of_imgs_to_be_saved(manwer.filelist) > 0
    wallpaper = myimage.number_of_imgs_to_be_wallpapered(manwer.filelist) > 0
    return (delete or save or wallpaper)

class Commit:
    def __init__(self, parent, event):
        self.parent = parent   # parent is manwer
        self.event  = event    # comes from manwer
        self.filelist = parent.filelist

    def start(self, confirmation = True):
        if there_is_something_to_commit(self.parent) == False:
            str = 'There is nothing to commit, there were no changes.'
            dial = wx.MessageDialog(None, str, 'Exclamation', wx.OK | wx.ICON_EXCLAMATION)
            dial.ShowModal()
            return
        if not self.parent.local_file:
            if self.parent.save_dir is None:
                str = "No save_dir is specified in your preferences."
                dial = wx.MessageDialog(None, str, 'Exclamation', wx.OK | wx.ICON_EXCLAMATION)
                dial.ShowModal()
                return
        # else
        if confirmation:
            dial = wx.MessageDialog(None, 'Do you want to commit your changes?', 'Question', 
                wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
            if dial.ShowModal() == wx.ID_NO:
                return
        # else
        self.save()
        self.delete()
        
    def save(self):
        if myimage.number_of_imgs_to_be_saved(self.filelist) == 0 \
            and myimage.number_of_imgs_to_be_wallpapered(self.filelist) == 0:
            return
        # else

        dir_name = None
        if myimage.number_of_imgs_to_be_saved(self.filelist) > 0:
            dir_name = os.path.join(self.parent.save_dir, self.parent.save_dir_relative)
            if os.path.exists(dir_name) == False:
                os.makedirs(dir_name)
        # OK, everything is ready to save the images
        down = download.Download(self)
        down.save_to_local(dir_name)
        
    def delete(self):
        if myimage.number_of_imgs_to_be_deleted(self.filelist) == 0:
            return
        # else
        
        li = self.parent.filelist
        curr_img = self.parent.filelist[self.parent.n]
        pos_img = None
        if curr_img.to_delete == False:   # the current image won't be deleted
            pos_img = curr_img
        else:   # if the current image will be removed
            not_to_be_deleted = [img for img in li[self.parent.n+1:] if not img.to_delete]
            if len(not_to_be_deleted) > 0:
                pos_img = not_to_be_deleted[0]
            else:
                not_to_be_deleted = [img for img in li[:self.parent.n] if not img.to_delete]
                if len(not_to_be_deleted) > 0:
                    pos_img = not_to_be_deleted[-1]
        # what to delete
        to_be_deleted = [img for img in li if img.to_delete]
        self.delete_physically(to_be_deleted)
        #
        li = [img for img in li if not img.to_delete]
        self.parent.filelist = li
        if len(li) > 0:
            index = li.index(pos_img)
            self.parent.n = index-1
            self.parent.on_next(self.event)
        else:
            self.parent.on_remove_queue(self.event)
            self.parent.dc.Refresh()
            
    def delete_physically(self, death_list):
        for img in death_list:
            os.remove(img.path)

####################

if __name__ == "__main__":
    pass
