import tkinter as tk


class StartWindow(object):

    def __init__(self, root, interface, world):
        super(StartWindow, self).__init__()
        self.root = root
        self.interface = interface
        self.world = world
        self.top = tk.Toplevel(self.root)
        self.top.title("Welcome to Forager1")

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.top.geometry('{}x{}+0+0'.format(self.screen_width, self.screen_height))

        self._canvas = tk.Canvas(self.top, width=self.screen_width, height=self.screen_height)
        self._canvas.grid()

        self._image = tk.PhotoImage(file='../images/start_screen.gif')
        self._canvas.create_image(0, 0, image=self._image, anchor=tk.NW)

        self.center_width = self.screen_width // 2
        self.center_height = self.screen_height // 2

        self._frame = tk.Frame(self.top)
        self._frame.grid(padx=10, pady=10)

        self._canvas.create_window(self.center_width, self.center_height + 50, width=240, height=80,
                                   anchor=tk.CENTER, window=self._frame)

        self._message = tk.Message(self._frame, justify=tk.CENTER, width=240,
                                   text="Welcome to Forager1, a turn-based game of hunting and gathering.")
        self._message.grid()

        self._start_button = tk.Button(self._frame, text="Start", command=self.start_button)
        self._start_button.grid(row=1, padx=40, sticky=tk.W)

        self._quit_button = tk.Button(self._frame, text="Quit", command=self.quit_button)
        self._quit_button.grid(row=1, padx=40, sticky=tk.E)

        self.top.transient(self.root)

    def start_button(self):
        self.world.start_day(self.top)

    def quit_button(self):
        exit()