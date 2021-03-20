from PyTyle.Tilers.TileDefault import TileDefault


class Maximal(TileDefault):
    def _tile(self):
        x, y, width, height = self.screen.get_workarea()

        for window in self.storage.get_masters() + self.storage.get_slaves():
            self.help_resize(
                window,
                x,
                y,
                width,
                height,
                self.state.get('margin')
            )

    def _cycle(self):
        pass

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


CLASS = Maximal
