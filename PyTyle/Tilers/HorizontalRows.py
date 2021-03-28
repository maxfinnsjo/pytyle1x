'''
This is something *like* the 'Horizontal' layout, except instead of having
one row of slaves 'beneath' the master, it can have multiple rows. By
default, it will be two windows per row (or, two columns). This can be
changed in the LAYOUT portion of the configuration file.
'''

from PyTyle.Tilers.TileDefault import TileDefault

import math


class HorizontalRows(TileDefault):
    # First we need to take care of our masters. Then we move the first row of
    # slaves up by the regular pixel amount. Then the second row gets moved up
    # by (pixels - (pixels/rows)). Each row gets a height increase of
    # pixels/rows.
    # Direction -1 for decrease, 1 for increase.
    def master_resize(self, direction: int, factor: float):
        x, y, width, height = self.screen.get_workarea()
        slaves = self.storage.get_slaves()
        masters = self.storage.get_masters()
        rowSize = self.state.get('row_size')
        rows = int(math.ceil(float(len(slaves)) / float(rowSize)))

        # Stop if neither of either
        if not slaves or not masters:
            return

        # first calculate pixels
        if direction > 0:
            pixels = int(
                (((self.state.get('height_factor') + factor) * height)
                    - (self.state.get('height_factor') * height))
            )
        else:
            pixels = int(
                ((self.state.get('height_factor') * height)
                    - ((self.state.get('height_factor') - factor) * height))
            )

        self.state.set(
            'height_factor',
            self.state.get('height_factor') + factor * direction
        )

        # Change pixels to next closest multiple of the number of rows
        pixels = pixels - (pixels % rows)
        slavePixels = pixels / rows

        currentRow = 1
        currentWindow = 1
        heightPixels = pixels
        for slave in slaves:
            slave.resize(
                slave.x,
                slave.y + heightPixels * direction,
                slave.width,
                slave.height - slavePixels * direction
            )

            if currentWindow % rowSize == 0:
                currentRow += 1
                currentWindow = 1
                heightPixels -= slavePixels
            else:
                currentWindow += 1
        for master in masters:
            master.resize(
                master.x,
                master.y,
                master.width,
                master.height + pixels * direction
            )

    # Does almost the same thing as the Horizontal layout,
    # but is a bit more complex to account for multiple
    # rows.
    def _tile(self):
        x, y, width, height = self.screen.get_workarea()

        masters = self.storage.get_masters()
        slaves = self.storage.get_slaves()
        rowSize = self.state.get('row_size')
        rows = int(math.ceil(float(len(slaves)) / float(rowSize)))
        lastRowSize = len(slaves) % rowSize
        if not lastRowSize:
            lastRowSize = rowSize

        masterWidth = width if not masters else (width / len(masters))
        masterHeight = height if not slaves else int(height * self.state.get('height_factor'))
        masterY = y
        masterX = x

        slaveWidth = width if not slaves else (width / rowSize)
        slaveHeight = height if not slaves else ((height if not masters else height - masterHeight) / rows)
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
                    't': masterY != y,
                    'l': masterX != x,
                    'r': masterX + masterWidth < x + width,
                    'b': masterY + masterHeight < y + height
                }
            )
            masterX += masterWidth

        currentRow = 1
        currentWindow = 1
        for slave in slaves:
            # last row!
            if currentRow == rows:
                slaveWidth = width / lastRowSize

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
                    'r': slaveWidth != width and currentWindow % rowSize != 0,
                    'b': slaveHeight != height and currentRow != rows
                }
            )
            slaveX += slaveWidth

            if currentWindow % rowSize == 0:
                currentRow += 1
                currentWindow = 1
                slaveX = x
                slaveY += slaveHeight
            else:
                currentWindow += 1

    def _master_increase(self, factor = 0.05):
        self.master_resize(1, factor)

    def _master_decrease(self, factor = 0.05):
        self.master_resize(-1, factor)

    # In HorizontalRows, the alignment of the masters is a bit weird. We would like
    # to have a consistent ordering style like so:
    # win --- win
    #       -
    #      -
    #     -
    # win --- win
    #       -
    #      -
    #     -
    # win --- win
    #
    # Note: See this method in Tile.TileDefault for additional comments.
    def help_find_next(self):
        masters = self.storage.get_masters()
        slaves = self.storage.get_slaves()
        all = masters + slaves

        if masters and self.screen.get_active().id == masters[-1].id:
            if not slaves:
                return masters[0]
            else:
                return slaves[0]
        elif slaves and self.screen.get_active().id == slaves[-1].id:
            if not masters:
                return slaves[0]
            else:
                return masters[0]
        elif slaves and self.screen.get_active().id in [win.id for win in slaves]:
            for i in range(len(slaves) - 1):
                if self.screen.get_active().id == slaves[i].id:
                    return slaves[(i + 1)]
        elif masters:
            for i in range(0, len(masters) - 1):
                if self.screen.get_active().id == masters[i].id:
                    return masters[(i + 1)]

    # See help_find_next above. Also see the comments in the code,
    # as help_find_previous is basically the same thing- we're just
    # going in reverse.
    def help_find_previous(self):
        masters = self.storage.get_masters()
        slaves = self.storage.get_slaves()
        all = masters + slaves

        if masters and self.screen.get_active().id == masters[0].id:
            if not slaves:
                return masters[-1]
            else:
                return slaves[-1]
        elif slaves and self.screen.get_active().id == slaves[0].id:
            if not masters:
                return slaves[-1]
            else:
                return masters[-1]
        elif masters and self.screen.get_active().id in [win.id for win in masters]:
            for i in range(1, len(masters)):
                if self.screen.get_active().id == masters[i].id:
                    return masters[(i - 1)]
        elif slaves:
            for i in range(1, len(slaves)):
                if self.screen.get_active().id == slaves[i].id:
                    return slaves[(i - 1)]


CLASS = HorizontalRows
