'''
The opposite to the Vertical layout. I like to use this on monitors with
1280x1024 (or 1920x1200) resolution, and Vertical on monitors with less
height to them (1280x720 or 1280x800).

This class inherits _cycle, help_find_next, and help_find_previous
from TileDefault.
'''

from PyTyle.Tilers.TileDefault import TileDefault


class Horizontal(TileDefault):
    # The core tiling algorithm. Every core tiling algorithm should start with
    # grabbing the current screen's workarea and factoring that into your
    # calculations. Feel free to follow my approach to tiling algorithms, or
    # come up with something else.
    def _tile(self):
        x, y, width, height = self.screen.get_workarea()
        masters = self.storage.get_masters()
        slaves = self.storage.get_slaves()

        masterWidth = width if not masters else (width / len(masters))
        masterHeight = height if not slaves else int(height * self.state.get('height_factor'))
        masterY = y
        masterX = x

        slaveWidth = width if not slaves else (width / len(slaves))
        slaveHeight = height if not masters else height - masterHeight
        slaveY = y if not masters else (y + masterHeight)
        slaveX = x

        # resize the master windows
        for master in masters:
            self.help_resize(
                master,
                masterX,
                masterY,
                masterWidth,
                masterHeight,
                self.state.get('margin'),
                self.state.get('internal_margin'),
                {
                    't': False,
                    'l': masterX != x,
                    'r': masterX + masterWidth < x + width,
                    'b': masterY + masterHeight < y + height
                }
            )
            masterX += masterWidth

        # now resize the rest... keep track of heights/positioning
        for slave in slaves:
            self.help_resize(
                slave,
                slaveX,
                slaveY,
                slaveWidth,
                slaveHeight,
                self.state.get('margin'),
                self.state.get('internal_margin'),
                {
                    't': slaveY != y,
                    'l': slaveX != x,
                    'r': slaveX + slaveWidth < x + width,
                    'b': False
                }
            )
            slaveX += slaveWidth

    #
    # Increases the height of all master windows. Don't forget to decrease
    # the height of all slave windows. Won't do anything if there are either
    # no masters or no slaves.
    #
    def _master_increase(self, factor = 0.05):
        x, y, width, height = self.screen.get_workarea()

        slaves = self.storage.get_slaves()
        masters = self.storage.get_masters()

        # Stop if neither of either... haha
        if not slaves or not masters:
            return

        # first calculate pixels...
        pixels = int(
            (((self.state.get('height_factor') + factor) * height)
                - (self.state.get('height_factor') * height))
        )
        self.state.set(
            'height_factor',
            self.state.get('height_factor') + factor
        )

        for slave in slaves:
            slave.resize(
                slave.x,
                slave.y + pixels,
                slave.width,
                slave.height - pixels
            )
        for master in masters:
            master.resize(
                master.x,
                master.y,
                master.width,
                master.height + pixels
            )

    # Decreases the height of all master windows. Don't forget to increase
    # the height of all slave windows. Won't do anything if there are either
    # no masters or no slaves.
    def _master_decrease(self, factor = 0.05):
        x, y, width, height = self.screen.get_workarea()

        slaves = self.storage.get_slaves()
        masters = self.storage.get_masters()

        # Stop if neither of either
        if not slaves or not masters:
            return

        # first calculate pixels
        pixels = int((self.state.get('height_factor') * height) - ((self.state.get('height_factor') - factor) * height))
        self.state.set('height_factor', self.state.get('height_factor') - factor)

        for slave in slaves:
            slave.resize(slave.x, slave.y - pixels, slave.width, slave.height + pixels)
        for master in masters:
            master.resize(master.x, master.y, master.width, master.height - pixels)


CLASS = Horizontal
