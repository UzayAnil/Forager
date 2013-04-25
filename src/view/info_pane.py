import tkinter as tk


class InfoPane(object):

    def __init__(self, root, canvas, world, player):
        super(InfoPane, self).__init__()
        self.player = player
        self._canvas = canvas
        self.world = world
        self._root = root
        self.info = tk.Toplevel(self._root)
        self.info.overrideredirect(True)

        self.screen_width = self._root.winfo_screenwidth()
        self.screen_height = self._root.winfo_screenheight()

        self.info.geometry("200x75+20+{}".format(self.screen_height - 120))
        self.info.transient(self._canvas)

        self.vigor_points = player.vigor_points
        self.wound_points = player.wound_points
        self.rounds = world.rounds

        self._frame = tk.Frame(self.info, padx=10, pady=10)
        self._frame.grid()

        self.screen_width = self._root.winfo_screenwidth()
        self.screen_height = self._root.winfo_screenheight()

        self.start_button = tk.Button(self._frame, text="End Turn", command=self.end_turn)
        self.start_button.grid(column=2, row=0, sticky=(tk.W, tk.N))

        self.round_label = tk.Label(self._frame, text="Round")
        self.round_label.grid(column=2, row=1, sticky=(tk.W, tk.S))

        self.round = tk.Message(self._frame, justify=tk.LEFT, text=str(self.rounds))
        self.round.grid(column=2, row=1, sticky=(tk.E, tk.N))

        self.vigor_label = tk.Label(self._frame, text="Vigor:")
        self.vigor_label.grid(column=0, row=0, sticky=tk.W)

        self.vigor = tk.Message(self._frame, justify=tk.LEFT, text=self.vigor_points)
        self.vigor.grid(column=1, row=0, sticky=tk.W)

        self.wound_label = tk.Label(self._frame, text="Wounds:")
        self.wound_label.grid(column=0, row=1, sticky=tk.W)

        self.wounds = tk.Message(self._frame, justify=tk.LEFT, text=self.wound_points)
        self.wounds.grid(column=1, row=1, sticky=tk.W)

    def end_turn(self):
        self.world.end_turn(self.info)