"""
Maximal.py

A very simply layout algorithm that allows for full screen windows. For the most
part, the only useful commands are screen focus/put and focusing on the
previous/next window.
"""

from PyTyle.Tilers.TileDefault import TileDefault

class Maximal (TileDefault):
    #------------------------------------------------------------------------------
    # OVERLOADED INSTANCE METHODS
    #------------------------------------------------------------------------------

    #
    # We don't need to cycle here- previous/next commands do it for us already.
    #
    def _cycle(self):
        pass

    #
    # This Maximal layout simply resizes every window to the screen's width and
    # height. (We aren't actually "maximizing" it here. This seemed to flow a
    # bit better with tiling in general.
    #
    def _tile(self):
        x, y, width, height = self.screen.get_workarea()

        # set some vars...
        masters = self.storage.get_masters()
        slaves = self.storage.get_slaves()

        masterWidth = width
        masterHeight = height
        masterY = y
        masterX = x

        slaveWidth = width
        slaveHeight = height
        slaveY = y
        slaveX = x

        # resize the master windows
        for master in masters:
            self.help_resize(master, masterX, masterY, masterWidth, masterHeight)

        # now resize the rest... keep track of heights/positioning
        for slave in slaves:
            self.help_resize(slave, slaveX, slaveY, slaveWidth, slaveHeight)

    #
    # We want to disable the following methods. They are of no use for this
    # layout.
    #
    def _master_increase(self, pixels = 50):
        pass

    def _master_decrease(self, pixels = 50):
        pass

    def _add_master(self):
        pass

    def _remove_master(self):
        pass

    def _make_active_master(self):
        pass

    def _win_master(self):
        pass

    def _switch_previous(self):
        pass

    def _switch_next(self):
        pass

    def _max_all(self):
        pass

    def _restore_all(self):
        pass

# You must have this line's equivalent for your tiling algorithm!
# This makes it possible to dynamically load tiling algorithms.
# (So that you may simply drop them into the Tilers directory,
# and add their name to the configuration- vini, vidi, vicci!)
CLASS = Maximal
