import tkinter as tk
from tkinter import ttk
from api_library import import_data

class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Loading")
        self.iconbitmap("./sources/icon.ico")
        self.minsize(250,100)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="Please wait..").pack()
        progressbar = ttk.Progressbar(self, length=200, mode='determinate', maximum=100)
        progressbar.pack()
        tk.Button(self, text="Cancel", command=self.close_window).pack()

        progressbar.step(20)
        progressbar.update()

        data = import_data("clan", "JP2VPJU")
        dict = {}

        progressbar.step(50)
        progressbar.update()

        for member in data["members"]:
            dict[member["tag"]] = member["name"]



        return dict



    def close_window(self):
        self.destroy()
        self.quit()


app = Window()
app.mainloop()