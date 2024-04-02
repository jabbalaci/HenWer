#!/usr/bin/env python

import os
import platform
import shutil
import urllib.error
import urllib.parse
import urllib.request

import myimage
import progressbar
import resources


class Download:
    def __init__(self, parent):
        self.parent = parent
        self.manwer = parent.parent
        self.referer = self.manwer.referer
        self.filelist = self.manwer.filelist
        all = myimage.number_of_imgs_to_be_saved(
            self.filelist
        ) + myimage.number_of_imgs_to_be_wallpapered(self.filelist)
        self.pbar = progressbar.Gauge(None, -1, "Saving images...", all)

    def save_to_local(self, dest_dir):
        cnt = 0
        we_have_a_saved_image = False
        for img in self.filelist:
            if img.to_save:  # dest_dir is needed
                self.get_image(dest_dir, img)
                we_have_a_saved_image = True
                img.to_save = False
                # update the progress bar
                cnt += 1
                self.pbar.set_value(cnt)
            if img.to_wallpaper:  # dest_dir is not needed
                self.get_wallpaper_image(img)
                img.to_wallpaper = False
                # update the progress bar
                cnt += 1
                self.pbar.set_value(cnt)
        self.manwer.set_status_text()
        #
        if we_have_a_saved_image:
            self.manwer.enable_menu(1, 0, True)  # enable switch to local

    def get_image(self, dest_dir, img):
        of = os.path.join(dest_dir, img.file_name)  # absolute path of output file name

        if self.referer is None:
            urllib.request.urlretrieve(img.path, of)
        else:
            req = urllib.request.Request(img.path)
            req.add_header("Referer", self.referer)
            response = urllib.request.urlopen(req)

            output = open(of, "wb")
            output.write(response.read())
            output.close()

    def get_wallpaper_image(self, img):
        # dest_dir exists and fine, we had already checked it
        dest_dir = resources.get_preferences(platform.system()).get("wallpapers_dir", None)
        fileName = myimage.get_timestamp() + img.file_ext
        of = os.path.join(dest_dir, fileName)  # absolute path of output file name

        if not img.local_file:  # not a local file, download it
            if self.referer is None:
                urllib.request.urlretrieve(img.path, of)
            else:
                req = urllib.request.Request(img.path)
                req.add_header("Referer", self.referer)
                response = urllib.request.urlopen(req)

                output = open(of, "wb")
                output.write(response.read())
                output.close()
        else:  # local file, copy it
            shutil.copy(img.path, of)


if __name__ == "__main__":
    pass
