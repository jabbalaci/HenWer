#!/usr/bin/env python

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

import os
import sys

package_dir = "lib"
package_dir_path = os.path.join(os.path.dirname(__file__), package_dir)
sys.path.insert(0, package_dir_path)


def process_command_line_parameter():
    """HenWer accepts a parameter that can be a directory path.
    HenWer will open then that directory upon startup."""
    if len(sys.argv) > 1:
        if sys.argv[1] == ".":
            sys.argv[1] = os.getcwd()
        elif os.path.isfile(sys.argv[1]):
            sys.argv[1] = os.path.join(os.getcwd(), sys.argv[1])

    os.chdir(os.path.dirname(__file__))


# process_command_line_parameter

process_command_line_parameter()  # call it


if __name__ == "__main__":
    import manwer
    import wx

    __version__ = manwer.__version__

    class ManWer(wx.App):
        def OnInit(self):
            self.frame = manwer.MReader("HenWer %s" % __version__)
            # self.tbicon = wx.TaskBarIcon()
            self.SetTopWindow(self.frame)
            self.SetExitOnFrameDelete(True)
            self.frame.Show()
            return True

    a = ManWer()
    a.MainLoop()
