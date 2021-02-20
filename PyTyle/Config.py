class Config:
    MISC = {}
    KEYMAP = {}
    WORKAREA = {}
    FILTER = []
    LAYOUT = {}
    TILING = {}
    TILERS = {}
    CALLBACKS = {}
    DEFAULTS = {
        'MISC': {
            'tilers': ['Vertical', 'Horizontal', 'Maximal', 'Cascade'],
            'global_tiling': False,
            'timeout': 0.1,
            'decorations': True,
            'original_decor': True,
        },
        'KEYMAP': {
            'Alt-A': 'tile.default',
            'Alt-U': 'untile',
            'Alt-Z': 'cycle_tiler',
            'Alt-Shift-space': 'reset',
            'Alt-C': 'cycle',
            'Alt-W': 'screen0_focus',
            'Alt-E': 'screen1_focus',
            'Alt-R': 'screen2_focus',
            'Alt-Shift-W': 'screen0_put',
            'Alt-Shift-E': 'screen1_put',
            'Alt-Shift-R': 'screen2_put',
            'Alt-H': 'master_decrease',
            'Alt-L': 'master_increase',
            'Alt-period': 'add_master',
            'Alt-comma': 'remove_master',
            'Alt-Return': 'make_active_master',
            'Alt-M': 'win_master',
            'Alt-Shift-C': 'win_close',
            'Alt-J': 'win_previous',
            'Alt-K': 'win_next',
            'Alt-Shift-J': 'switch_previous',
            'Alt-Shift-K': 'switch_next',
            'Alt-X': 'max_all',
            'Alt-S': 'restore_all',
        },
        'WORKAREA': {
            0: {
                'top': 0,
                'bottom': 0,
                'right': 0,
                'left': 0,
            },
        },
        'FILTER': [
            'gmrun', 'gimp', 'download'
        ],
        'LAYOUT': {
            'Vertical': {
                'width_factor': 0.5,
                'margin': 0,
            },
            'Horizontal': {
                'height_factor': 0.5,
                'margin': 0,
            },
            'Maximal': {},
            'Cascade': {
                'decoration_height': 25,
                'width_factor': 1.0,
                'height_factor': 1.0,
                'push_over': 0,
                'horz_align': 'left',
            },
            'HorizontalRows': {
                'row_size': 2,
                'height_factor': 0.5,
                'margin': 0,
            },
        },
        'TILING': {
            'default': 'Vertical',
        }
    }

    @staticmethod
    def misc(name):
        if name in Config.MISC:
            return Config.MISC[name]

        if name in Config.DEFAULTS['MISC']:
            return Config.DEFAULTS['MISC'][name]

        return None

    @staticmethod
    def keymap(keys):
        if keys in Config.KEYMAP:
            return Config.KEYMAP[keys]

        if keys in Config.DEFAULTS['KEYMAP']:
            return Config.DEFAULTS['KEYMAP'][keys]

        return None

    @staticmethod
    def workarea(screenNum, section):
        if screenNum in Config.WORKAREA and section in Config.WORKAREA[screenNum]:
            return Config.WORKAREA[screenNum][section]

        return Config.DEFAULTS['WORKAREA'][0][section]

    @staticmethod
    def filter():
        return Config.FILTER

    @staticmethod
    def layout(tiler, option):
        layout = tiler.__class__.__name__
        if layout in Config.LAYOUT and option in Config.LAYOUT[layout]:
            return Config.LAYOUT[layout][option]

        if layout in Config.DEFAULTS['LAYOUT'] and option in Config.DEFAULTS['LAYOUT'][layout]:
            return Config.DEFAULTS['LAYOUT'][layout][option]

        return None

    @staticmethod
    def tiling(screen, deskOrView):
        if screen in Config.TILING:
            if isinstance(Config.TILING[screen], dict) and deskOrView in Config.TILING[screen]:
                return Config.TILING[screen][deskOrView]
            elif not isinstance(Config.TILING[screen], dict):
                return Config.TILING[screen]
        elif 'default' in Config.TILING:
            return Config.TILING['default']

        return Config.DEFAULTS['TILING']['default']

    @staticmethod
    def tilers(layout):
        if layout in Config.TILERS:
            return Config.TILERS[layout]

    # Special flag to enable/disable debugging
    DEBUG = False
