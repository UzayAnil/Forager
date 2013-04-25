import tkinter as tk
from tkinter import ttk


class Interface(object):

    def __init__(self, width=2560, height=2560, game_world=None, **kwargs):
        super(Interface, self).__init__(**kwargs)
        self._root = tk.Tk()
        self.title = self._root.title("Forager1")
        self._world = None

        # Building the scrollbars
        self.horizontal = ttk.Scrollbar(self._root, orient=tk.HORIZONTAL)
        self.vertical = ttk.Scrollbar(self._root, orient=tk.VERTICAL)

        self.screen_width = self._root.winfo_screenwidth()
        self.screen_height = self._root.winfo_screenheight()

        # Building the canvas
        self._canvas = tk.Canvas(self._root, scrollregion=(0, 0, width, height), width=self.screen_width,
                                 height=self.screen_height, yscrollcommand=self.vertical.set,
                                 xscrollcommand=self.horizontal.set)

        # Scrolling management
        self.horizontal['command'] = self._canvas.xview
        self.vertical['command'] = self._canvas.yview

        # Arrange the pieces on the grid
        self._canvas.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.horizontal.grid(column=0, row=1, sticky=(tk.W, tk.E))
        self.vertical.grid(column=1, row=0, sticky=(tk.N, tk.S))
        self._root.grid_columnconfigure(0, weight=1)
        self._root.grid_rowconfigure(0, weight=1)

        # Bind the
        self._canvas.bind('<Button-1>', self.click_handler)
        self._canvas.bind('<Motion>', self.cursor_motion)
        self._root.bind('<Key>', self.key_press)

        self.text_list = list()
        self._col = 0
        self._row = 0
        self._creature_list = list()

    def start_game(self, start_window):
        start_window.destroy()
        self.world.day(1, self.creature_list)

    def end_turn(self):
        self.human = self.world._player
        self.human.end_turn.set(1)

    @property
    def world(self):
        return self._world

    @world.setter
    def world(self, world):
        assert self._world is None
        self._world = world

    @property
    def creature_list(self):
        return self._creature_list

    @creature_list.setter
    def creature_list(self, creature_list):
        self._creature_list = creature_list

    @property
    def canvas(self):
        return self._canvas

    def redraw(self, drawable_list):
        self._canvas.delete(tk.ALL)
        for element in drawable_list:
            self._canvas.create_image(element.position_col, element.position_row,
                                      image=element.get_sprite(), anchor=tk.CENTER)
        self._root.update()

    def action_text(self, creature):
        """Action Text

        Draws Attack! above an attacked creature.

        """
        target = creature.target
        text = self._canvas.create_text(target.position_col, target.position_row - 20, fill="red", text="Attack!")
        self.world.add_text_object(text)
        self.text_list.append(text)

    def click_handler(self, event):
        """Click Handler

        Passes the event to the world.

        """
        self.world.player_action(event)

    def scrolling_handler(self):
        """Scrolling Handler

        Scrolls the window when the cursor is near the screen edges.

        """
        col = self._col
        row = self._row
        canvas = self._canvas

        if col < 64:
            number = -1
            canvas.xview_scroll(number, 'units')
        elif col > (self._canvas.winfo_screenwidth() - 64):
            number = 1
            canvas.xview_scroll(number, 'units')

        elif row < 64:
            number = -1
            canvas.yview_scroll(number, 'units')
        elif row > (self._canvas.winfo_screenheight() - 100):
            number = 1
            canvas.yview_scroll(number, 'units')

        canvas.after(100, self.scrolling_handler)

    def cursor_motion(self, event):
        """Cursor Motion

        Captures cursor motion and stores it for the scrolling handler.

        """
        self._col = event.x
        self._row = event.y

    def key_press(self, event):
        """Key Press

        Detects key presses and runs the appropriate methods.

        """
        if event.keysym == "Return":
            self.world.info_pane.end_turn()
        if (event.keysym == "w" or event.keysym == "r" or event.keysym == "s" or
                event.keysym == "h" or event.keysym == "o"):
            self.world.change_move(event.keysym)
        if event.keysym == "Escape":
            print("Goodbye.")
            exit()