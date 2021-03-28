'''
Performs a full screen cascading layout of all the windows. It's important that
we're able to access the window decoration sizes.
'''

from PyTyle.Tilers.TileDefault import TileDefault

class Cascade(TileDefault):
    # This Cascade layout will essentially do the following:
    #    1. The first window (or bottom) window takes up the full screen.
    #    2. Each subsequent window has its height shrinked by the height of
    #       the window decoration.
    def _tile(self):
        x, y, width, height = self.screen.get_workarea()
        masters = self.storage.get_masters()
        slaves = self.storage.get_slaves()

        # If we don't have any decorations... use hard coded value for now
        if masters and masters[0].d_top:
            decor = masters[0].d_top
        elif slaves and slaves[0].d_top:
            decor = slaves[0].d_top
        else:
            decor = self.state.get('decoration_height')

        push_over = self.state.get('push_over')
        push_width = push_over
        if self.state.get('horz_align') == 'right':
            push_over = -push_over

        masterWidth = ((width * self.state.get('width_factor'))
            - (push_width * len(slaves)))
        masterHeight = ((height * self.state.get('height_factor'))
            - (decor * len(slaves)))
        masterY = y + (decor * len(slaves))

        slaveWidth = width * self.state.get('width_factor')
        slaveHeight = height * self.state.get('height_factor')
        slaveY = y

        if self.state.get('horz_align') == 'right':
            masterX = x + (width - masterWidth) + (push_over * len(slaves))
            slaveX = x + (width - slaveWidth)
            push_over = 0
        else:
            masterX = x + (push_over * len(slaves))
            slaveX = x

        # now resize the rest... keep track of heights/positioning
        for slave in slaves:
            self.help_resize(slave, slaveX, slaveY, slaveWidth, slaveHeight)
            slaveY += decor
            slaveHeight -= decor
            slaveWidth -= push_width
            slaveX += push_over
            slave.stack_raise()

        # resize the master windows
        for master in masters:
            self.help_resize(master, masterX, masterY, masterWidth, masterHeight)
            master.stack_raise()

        # just in case...
        self.screen.get_active().stack_raise()

    # Not changing much functionality here. Just overloading, inheriting, and
    # making sure the stacking order is kept.
    def _cycle(self):
        TileDefault._cycle(self)
        self.help_reset_stack()

    def _make_active_master(self):
        TileDefault._make_active_master(self)
        self.help_reset_stack()

    def _win_master(self):
        TileDefault._win_master(self)
        self.help_reset_stack()

    def _win_previous(self):
        self.help_find_previous().activate()
        self.help_reset_stack()

    def _switch_previous(self):
        TileDefault._switch_previous(self)
        self.help_reset_stack()

    def _switch_next(self):
        TileDefault._switch_next(self)
        self.help_reset_stack()

    # We want to disable the following methods. They are of no use for this
    # layout.
    def _master_increase(self, pixels = 50):
        pass

    def _master_decrease(self, pixels = 50):
        pass

    def _add_master(self):
        pass

    def _remove_master(self):
        pass

    # Same exact thing as Tile.help_reload, except we add to the top
    # of the window stack instead.
    def help_reload(self):
        # delete first...
        for win in self.storage.get_all():
            if win.id not in self.screen.windows or win.hidden:
                self.storage.remove(win)

        masters = self.storage.get_masters_by_id()

        if self.screen.get_active() and len(masters) < self.storage.get_master_count() and self.screen.get_active().id in self.screen.windows and self.screen.get_active().id not in masters:
            self.storage.remove(self.screen.get_active())
            self.storage.add(self.screen.get_active())
            masters = self.storage.get_masters_by_id()

        all = self.storage.get_all_by_id()
        for window in self.screen.windows.values():
            if not window.id in all:
                self.storage.add_top(window)
            else:
                self.storage.try_to_promote(window)

    # Resets the stacking order
    def help_reset_stack(self):
        masters = self.storage.get_masters()
        slaves = self.storage.get_slaves()

        # now set the stacking order straight
        for slave in slaves:
            slave.stack_raise()
        self.screen.get_active().stack_raise()


CLASS = Cascade
