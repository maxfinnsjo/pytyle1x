'''
The most basic and default tiling algorithm. It consists of a master pane
on the left, and keeps the slaves over to the right.

Remember that this class inherits _cycle, help_find_next, and help_find_previous
from TileDefault.
'''

from PyTyle.Tilers.TileDefault import TileDefault


class Vertical(TileDefault):
    # Direction -1 for decrease, 1 for increase
    def master_resize(self, direction: int, factor: float):
        x, y, width, height = self.screen.get_workarea()
        slaves = self.storage.get_slaves()
        masters = self.storage.get_masters()

        # Stop if neither of either
        if not slaves or not masters:
            return

        # first calculate pixels
        if direction > 0:
            pixels = int(
                (((self.state.get('width_factor') + factor) * width)
                    - (self.state.get('width_factor') * width))
            )
        else:
            pixels = int(
                ((self.state.get('width_factor') * width)
                    - ((self.state.get('width_factor') - factor) * width))
            )

        self.state.set(
            'width_factor',
            self.state.get('width_factor') + factor * direction
        )

        for slave in slaves:
            slave.resize(
                slave.x + pixels * direction,
                slave.y,
                slave.width - pixels * direction,
                slave.height
            )
        for master in masters:
            master.resize(
                master.x,
                master.y,
                master.width + pixels * direction,
                master.height
            )

    # The core tiling algorithm. Every core tiling algorithm should start with
    # grabbing the current screen's workarea and factoring that into your
    # calculations. Feel free to follow my approach to tiling algorithms, or
    # come up with something else.
    def _tile(self):
        x, y, width, height = self.screen.get_workarea()

        masters = self.storage.get_masters()
        slaves = self.storage.get_slaves()

        masterWidth = width if not slaves else int(width * self.state.get('width_factor'))
        masterHeight = height if not masters else (height / len(masters))
        masterY = y
        masterX = x

        slaveWidth = width if not masters else width - masterWidth
        slaveHeight = height if not slaves else (height / len(slaves))
        slaveY = y
        slaveX = x if not masters else (x + masterWidth)

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
                    't': masterY != y,
                    'l': False,
                    'r': masterX + masterWidth < x + width,
                    'b': masterY + masterHeight < y + height
                }
            )
            masterY += masterHeight

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
                    'r': False,
                    'b': slaveY + slaveHeight < y + height
                }
            )
            slaveY += slaveHeight

    # Increases the width of all master windows.
    def _master_increase(self, factor = 0.05):
        self.master_resize(1, factor)

    # Decreases the width of all master windows.
    def _master_decrease(self, factor = 0.05):
        self.master_resize(-1, factor)


CLASS = Vertical
