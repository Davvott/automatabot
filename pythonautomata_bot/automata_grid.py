from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import StringVar

MAX_WIN_WIDTH = 1100
MAX_WIN_HEIGHT = 900


class Toolbar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.toolbar_frame = ttk.LabelFrame(self.parent, text='AutomataBot', padding=(5, 5, 5, 5), height=40)
        self.toolbar_frame.pack(side='top', fill='x')

        self.toolbar = ttk.Label(
            self.toolbar_frame, textvariable=self.parent._game_type, padding=(2, 2, 2, 2),
            justify='center')
        self.toolbar.pack(side='top', fill='y', anchor="n")


class GridBox(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Init Grid variables
        _c = self.parent.cols
        _r = self.parent.rows

        self.cellheight = MAX_WIN_HEIGHT / _r
        self.cellwidth = self.cellheight

        # Creating Canvas larger than grid
        self.wide = self.cellwidth*_c
        self.high = self.cellheight*_r

        self.canvas_frame = ttk.Frame(self.parent, padding=(2, 2, 2, 2))
        self.canvas_frame.pack(side='top', fill='both')
        self.canvas = tk.Canvas(
            self.canvas_frame, width=self.wide, height=self.high, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")

        # Initialize Grid
        self.grid = {}
        for row in range(_r):
            for col in range(_c):
                x1 = col * self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                # Each grid item will return an item_id
                self.grid[(row, col)] = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill="white", tags=("rect", 'white'))


class OptionsBox(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Labels, Buttons, Entry's
        self.options_frame = ttk.LabelFrame(self.parent, text='Options', width=100, padding=(5, 5, 5, 5))
        self.options_frame.pack(side='right', fill='y', expand=True)


class Main(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)


class MainApp(tk.Frame):
    """Builds GUI for Game of Life, requires Automata class"""
    def __init__(self, parent, bot, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # initialize variables
        self._game_type = StringVar()
        title = "Game of Life\n {}".format(bot.__str__())
        self._game_type.set(title)

        self._delay = IntVar()
        self._delay = 500

        self.cols = IntVar()
        self.rows = IntVar()
        self.cols = bot.cols
        self.rows = bot.rows
        self.year = 0

        # Instantiate Frames
        self.toolbar = Toolbar(self)  # instantiates class in order
        # self.options_box = OptionsBox(self)
        self.gridbox = GridBox(self)
        self.main = Main(self)

        self.toolbar.pack(side="top", fill="x", padx=5, pady=5)
        self.gridbox.pack(side='top', fill='both', expand=True, padx=5, pady=5)
        # self.options_box.pack(side="right", fill="y")
        self.main.pack(side="right", fill="both", expand=True)

        self.automata = bot

        self.run()

    def run(self):
        self.wipe_grid()
        self.initialise_grid()
        self.after(self._delay, lambda: self.redraw(self._delay))

    def redraw(self, delay):
        # type(black_tiles) = <class 'tuple'> of item_ids
        # grid -> dict{(y, x): item_id,}

        alive_cells = self.gridbox.canvas.find_withtag('black')
        tiles_to_change = self.automata.next_state()  # list

        for tile in tiles_to_change:
            item_id = self.gridbox.grid[(tile[0], tile[1])]

            if item_id not in alive_cells:
                self.gridbox.canvas.itemconfig(
                    item_id, fill="black", tags=('rect', 'black'))
            else:
                self.gridbox.canvas.itemconfig(
                    item_id, fill="white", tags=('rect', 'white'))

        self.after(delay, lambda: self.redraw(delay))

    def initialise_grid(self):
        """Initialises Grid from automata cell state"""
        alive_cells = self.automata.get_alive_cells()

        for tile in alive_cells:
            item_id = self.gridbox.grid[(tile[0], tile[1])]
            self.gridbox.canvas.itemconfig(item_id, fill="black", tags=('rect', 'black'))

    def wipe_grid(self):
        """WIPE GRID - reset all items with tag='rect'"""
        self.gridbox.canvas.itemconfig(
            "rect", fill="white", tags=('rect', 'white'))
