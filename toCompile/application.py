import matplotlib
matplotlib.use("TkAgg")
from os import listdir
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from tkinter import messagebox
from matplotlib import pyplot as plt
from datetime import datetime
from tkinter import *
from copy import deepcopy
import numpy as np
from PIL import Image, ImageTk
from tkinter import ttk
import sys
import time
import clan_war_decks_import, war_log_import, top_played_cards


import api_library

HEADER_FONT = ("Verdana", 12)
TABLE_HUGE_FONT = ("Candara", 30)
style.use(style.available[14])
f = plt.figure()
#member_dict = api_library.member_dict()
#print(member_dict)
member_dict = {'8922R8Q2': ['RealHero', '#DE8817'], '20VUQ8UL9': ['lord Solrak', '#7C5540'], 'CLYVV0JU': ['NejSemTu', '#D9FA61'], 'LQL99J2U': ['SUPERCELL', '#37896E'], 'YC8R8JGY': ['Mr. Kev', '#9BBE47'], '9CUYJJ8G': ['Srej', '#27E7B9'], '9PG8QRGV': ['Mike PB', '#9B8CE4'], '9LVGRL80': ['Daník009cz', '#E635EF'], 'CLQG82LP': ['sirrizek', '#707401'], 'QUG02C8': ['Shaunus', '#AE0054'], '99PPJLY8': ['Sweetboy', '#5B2752'], '8V8009VJ': ['TacheraBanana', '#0978CE'], '820PVJR9': ['HANCIK', '#223786'], 'UY0UJLQ9': ['DonPepe', '#D4DA20'], '9YQUQ928': ['Satan ', '#E785EF'], '229YQU9J': ['pioter', '#D9E299'], '9200UJL2L': ['McAlda', '#760B4D'], '2CLVUC9UV': ['Karasek', '#DD08D0'], 'LJ0P8G0': ['bambuchy', '#A5CEE9'], '8R00Y2820': ['pakoCZ', '#3A29A4'], '890RP02CQ': ['Esuba Krťofiloš', '#A42945'], '8CRUR2RVP': ['machajda vole', '#94AF24'], '2L98RYC2J': ['Eskel', '#A45133'], '28R82C022': ['MatyNovyCZ', '#2FBBDD'], '2PU22P2GJ': ['vovo', '#B509D8'], 'QR0U8U2P': ['jedlevit', '#D71656'], '2PPQJ2VCJ': ['Deadpool', '#AF8D04'], '9VLG0GJP': ['valuee', '#AAF093'], '28UVQQLCU': ['Liskalord21', '#9DF346'], '2CPRCURQJ': ['mikes3', '#5C7BEF'], 'UCL20R22': ['kubik formik', '#705809'], '8ULGR0V0G': ['Zadet Danda', '#C926C8'], '8Y98QPPVC': ['proyesCZ', '#0EB4EE'], '8GC8908Y': ['Qetrax', '#9FA4BC'], '8VQ0UR9LR': ['trvka 16', '#30D917'], 'PCL2QYP2': ['Joker', '#D372B8'], 'LQ90RU8Q': ['AweXíK', '#C8895C'], '828RVQJCL': ['Vladutu', '#AAA1A2'], '8UVYU088U': ['hubis', '#728E3C'], 'PLRCYC8Y': ['Dual GG', '#2CC061'], '8RJ2ULJQV': ['amoos', '#CC7DD7'], '80UUCGG8Y': ['Crooasant YT :D', '#52099B'], '90PGU8P': ['jenda', '#0AECA9'], '2C2YUQ2R9': ['hermanpeta', '#4C9AF7']}

lined = {}
lines = []



def onpick(event):
    # on the pick event, find the orig line corresponding to the
    # legend proxy line, and toggle the visibility
    legline = event.artist
    origline = lined[legline]
    vis = not origline[0].get_visible()
    origline[0].set_visible(vis)
    # Change the alpha on the line in the legend so we can see what lines
    # have been toggled
    if vis:
        legline.set_alpha(1.0)
    else:
        legline.set_alpha(0.2)
    f.canvas.draw()

def backup():
    data = ["cw_battle_res.txt", "data.txt", "top_synergy.txt", "cw_battle_deck_monster.txt", "cw_battle_deck_6a6.txt"]
    for file in listdir("./data"):
        orig = open("./data/"+file, "r")
        content = orig.read()
        output = open("./zaloha/"+file, "w+")
        output.write(content)
        output.close()
        orig.close()
    messagebox.showinfo("Info", "Backup was made")
def popmsg(msg):
    messagebox.showinfo("Info", msg)

class App(Toplevel):
    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        self.title("ApiRoyale")
        self.iconbitmap("./sources/icon.ico")

        container = Frame(self)
        container.pack(side="top", fill="both", expand = True)
        #container.grid(row=0, column=0, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.images = {}
        self.constants = api_library.import_data("constants")
        self.cards = sorted([x["name"] for x in self.constants["cards"]])
        self.cards_file_name = {}
        self.cards_file_name_init()
        self.frames = {}
        for F in (StartPage, ImportPage, InRowGraph, CWSynergyCards):
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        menubar = Menu(container)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Home", command=lambda: self.show_frame(StartPage))
        filemenu.add_command(label="Data Backup", command=backup)
        filemenu.add_command(label="Data Import", command=lambda: self.show_frame(ImportPage))
        filemenu.add_command(label="Save Setting", command=lambda: popmsg("Not supported yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=sys.exit)
        menubar.add_cascade(label="File", menu=filemenu)

        graphmenu = Menu(menubar, tearoff=0)
        graphmenu.add_command(label="Clan War.Wins/Losses in row", command=lambda: self.show_frame(InRowGraph))
        graphmenu.add_command(label="Clan War.Cards synergy", command=lambda: popmsg("Not supported yet!"))
        menubar.add_cascade(label="Graphs", menu=graphmenu)

        tablemenu = Menu(menubar, tearoff=0)
        tablemenu.add_command(label="Clan War.Synergy Cards", command=lambda: self.show_frame(CWSynergyCards))
        menubar.add_cascade(label="Synergy", menu=tablemenu)

        Tk.config(self, menu=menubar)
        #self.show_frame(StartPage)
        self.show_frame(CWSynergyCards)

    def show_frame(self, cont):
        frame = self.frames[cont]
        if frame.__class__.__name__ in ["InRowGraph", "CWSynergyCards"]:
            frame.show()
        frame.tkraise()

    def load_images(self):
        for image in listdir("./sources/images/cards"):
            img = Image.open("./sources/images/cards/" + image)
            self.images[image[:-4]] = img.resize((75, 100))

    def cards_file_name_init(self):
        for i in self.constants["cards"]:
            self.cards_file_name[i["id"]] = i["key"]


class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Start Page", font=HEADER_FONT)
        label.pack(pady=10, padx=10)

        button1 = Button(self, text="Import Page", command = lambda: controller.show_frame(ImportPage))
        button1.pack()
        button2 = Button(self, text="Graph Page", command=lambda: controller.show_frame(InRowGraph))
        button2.pack()

class ImportPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Import Page", font=HEADER_FONT)
        label.pack(pady=10, padx=10)

        button1 = Button(self, text="Start Page", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = Button(self, text="Graph Page", command=lambda: controller.show_frame(InRowGraph))
        button2.pack()

        self.importing = False

        self.entrys = []
        for i in range(5):
            self.entrys.append(StringVar(parent))

        self.checkboxes = []  # five checkboxes
        for i in range(5):
            self.checkboxes.append(IntVar(parent))

        Checkbutton(self, text="Clan War Decks", variable=self.checkboxes[0]).pack()
        self.entry0 = Entry(self, textvariable=self.entrys[0])
        self.entry0.pack()
        self.entry0.insert(0, "cw_battle_deck_6a6.txt")

        Checkbutton(self, text="Clan War Logs", variable=self.checkboxes[1]).pack()
        self.entry1 = Entry(self, textvariable=self.entrys[1])
        self.entry1.pack()
        self.entry1.insert(0, "cw_battle_res_6a6.txt")

        Button(self, command=self.import_data, text="import").pack()

    def import_data(self):
        self.entry1.update_idletasks()
        self.entry1.update()
        if not self.importing:
            data = [clan_war_decks_import.run, war_log_import.run]
            self.importing = True
            for i in range(2):
                print(self.checkboxes[i].get())
                print(self.entrys[i].get())
                if self.checkboxes[i].get():
                    data[i]("./data/" + self.entrys[i].get())
            self.importing = False

class InRowGraph(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.header = EmptyFrame(self, controller)
        self.header.pack(anchor=W)
        
        self.legend_counter = 0
        self.tmp_box = []

        self.var_type = IntVar(parent)
        self.var_type.set(1)
        self.var_type1 = IntVar(parent)
        self.var_type1.set(1)
        
        self.var_boundary = StringVar(parent)
        self.var_boundary.set("5")

        Label(self.header, text="In Row Graph", font=HEADER_FONT).grid(column=0, row=0, columnspan=2)
        Label(self.header, text="Boundary: ").grid(column=0, row=1)
        Entry(self.header, textvariable=self.var_boundary, width=12).grid(column=1, row=1)
        Radiobutton(self.header, text="Wins", variable=self.var_type, value=1, bg="#F5A9A9", width=8).grid(column=2, row=1)
        Radiobutton(self.header, text="Losses", variable=self.var_type, value=2, bg="#F5A9A9", width=8).grid(column=3, row=1)
        Radiobutton(self.header, text="Both", variable=self.var_type, value=3, bg="#F5A9A9", width=8).grid(column=4, row=1)
        Radiobutton(self.header, text="Timeline", variable=self.var_type1, value=1, bg="#A9D0F5", width=8).grid(column=5, row=1)
        Radiobutton(self.header, text="Bar", variable=self.var_type1, value=2, bg="#A9D0F5", width=8).grid(column=6, row=1)
        Button(self.header, text="Show!", command=self.show, width=11).grid(column=7, row=1)

        self.canvas = FigureCanvasTkAgg(f, self)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
    def box_init(self):
        pullData = open("./data/cw_battle_res_6a6.txt", "r").read()
        dataList = pullData.split("\n")
        self.legend_counter = 0
        self.tmp_box = []
        dates = [datetime.fromtimestamp(int(dataList[1].split("\t")[x])).strftime("%B %d") for x in
                 range(1, len(dataList[1].split("\t")))]
        for index in range(2, len(dataList)):
            dataList[index] = dataList[index].split("\t")
            x_list = [0] + dates
            y_list = [0]
            api_library.process_in_row(y_list, dataList[index], self.var_type.get())
            self.legend_counter += 1
            member_box = []
            member_box.append(dataList[index][0])
            member_box.append(x_list)
            member_box.append(y_list)
            self.tmp_box.append(member_box)

    def show(self):
        try:
            boundary = int(self.var_boundary.get())
        except ValueError:
            messagebox.showinfo("Error", "Bad parameter")
            return 1
        if self.tmp_box == []:
            self.box_init()
        set_box = deepcopy(self.tmp_box)
        if self.var_type.get() == 1:
            for member in set_box:
                for i in range(len(member[2])):
                    if member[2][i] >= 0:
                        pass
                    else:
                        member[2][i] = 0

        if self.var_type.get() == 2:
            for member in set_box:
                for i in range(len(member[2])):
                    if member[2][i] <= 0:
                        member[2][i] = -(member[2][i])
                    else:
                        member[2][i] = 0
        tmp = []
        in_box_counter = 0
        y_max = 1
        y_min = 0
        for member in set_box:
            if max(member[2]) >= int(self.var_boundary.get()) or -min(member[2]) >= int(self.var_boundary.get()):
                tmp.append(member)
                in_box_counter += 1
            if max(member[2]) > y_max:
                y_max = max(member[2])
            if min(member[2]) < y_min:
                y_min = min(member[2])
        set_box = tmp
        f.clear()
        if self.var_type1.get() == 1:
            a = f.add_axes([0.05, 0.13 + 0.045 * (in_box_counter // 7), 0.90, 0.85 - (0.045 * (in_box_counter // 7))])
            plt.xlim((len(set_box[0][1]) - 10, len(set_box[0][1]) - 1))
            lines.clear()
            for index in range(0, len(set_box)):
                lines.append(a.plot(set_box[index][1], set_box[index][2], label=member_dict[set_box[index][0]][0], color=member_dict[set_box[index][0]][1]))

            leg = a.legend(bbox_to_anchor=(0, -0.27, 0, 0.2), loc=2, ncol=7, fancybox=True)
            for legline, origline in zip(leg.get_lines(), lines):
                legline.set_picker(5)  # 5 pts tolerance
                lined[legline] = origline

            self.canvas.mpl_connect('pick_event', onpick)
        else:
            if in_box_counter > 9:
                a = f.add_axes([0.05, 0.25, 0.90, 0.72])
            else:
                a = f.add_axes([0.05, 0.1, 0.90, 0.87])
            counter = 0
            set_box.sort(key=lambda x: max(x[2]) + min(x[2]))
            set_box.reverse()
            for member in range(0, len(set_box)):
                counter += 1
                a.bar(counter, [0, max(set_box[member][2])], color=member_dict[set_box[member][0]][1])
                a.bar(counter, [min(set_box[member][2]), 0], color=member_dict[set_box[member][0]][1])
            a.axhline(y=0, color='black')
            if in_box_counter >9:
                plt.xticks(np.arange((len(set_box)) + 1), [" "] + [member_dict[set_box[x][0]][0] for x in range(0, len(set_box))], rotation=90)
            else:
                plt.xticks(np.arange(len(set_box) + 1), [" "] + [member_dict[set_box[x][0]][0] for x in range(0, len(set_box))])
        plt.yticks(range(y_min, y_max+1))
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=BOTTOM, fill=BOTH, expand=True)


class CWSynergyCards(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.header = EmptyFrame(self, controller)
        self.header.config(padx=15)
        self.header.pack(side="left", anchor=N)
        if self.controller.images == {}:
            self.controller.load_images()
        self.var_type = IntVar(parent)
        self.var_type.set(1)
        self.var_type1 = IntVar(parent)
        self.var_type1.set(1)

        self.var_cards = StringVar(parent)
        self.var_cards.set("2")

        self.var_val_days = StringVar(parent)
        self.var_val_days.set("100")

        self.var_games = StringVar(parent)
        self.var_games.set("10")

        self.var_sort = IntVar(parent)
        self.var_sort.set(2)
        self.var_sort2 = IntVar(parent)
        self.var_sort.set(0)

        Label(self.header, text="CW Synergy Cards", font=HEADER_FONT).grid(column=0, row=0, columnspan=3)
        Label(self.header, text="Cards in synergy: ").grid(column=0, row=1, sticky=W)
        Entry(self.header, textvariable=self.var_cards, width=5).grid(column=2, row=1, sticky=W)
        Label(self.header, text="Day of Validity: ").grid(column=0, row=2, columnspan=2, sticky=W)
        Entry(self.header, textvariable=self.var_val_days, width=5).grid(column=2, row=2, sticky=W)
        Label(self.header, text="Minimum games: ").grid(column=0, row=3, columnspan=2, sticky=W)
        Entry(self.header, textvariable=self.var_games, width=5).grid(column=2, row=3, sticky=W)

        sort_by_block = EmptyFrame(self.header, self.controller)
        sort_by_block.grid(column=0, row=4, sticky=W, columnspan=3)
        Label(sort_by_block, text="Sorted by: ").grid(column = 0, row = 0)
        Radiobutton(sort_by_block, text="Rate", variable=self.var_sort, value=2, bg="#F5A9A9", width=8).grid(column=1,
                                                                                                           row=0)
        Radiobutton(sort_by_block, text="Wins", variable=self.var_sort, value=0, bg="#F5A9A9", width=8).grid(column=1,
                                                                                                             row=1)
        Radiobutton(sort_by_block, text="Losses", variable=self.var_sort, value=1, bg="#F5A9A9", width=8).grid(column=1,
                                                                                                           row=2)
        Radiobutton(sort_by_block, text="Descending", variable=self.var_sort2, value=0, bg="green", width=8).grid(column=0,
                                                                                                             row=1)
        Radiobutton(sort_by_block, text="Ascending", variable=self.var_sort2, value=1, bg="green", width=8).grid(column=0,
                                                                                                             row=2)

        variable = StringVar(parent)
        variable.set('None')

        w = OptionMenu(self.header, variable, *(["None"] + self.controller.cards))
        w.grid(column=0, row=9, sticky=W)

        Button(self.header, text="Show!", width=11, command=self.show).grid(column=0, row=10, columnspan=3)


        #scrolling table config
        self.table_figure = EmptyFrame(self, self.controller)
        self.table_figure.pack(expand=True, fill="both", side="left", anchor=N)
        self.table_canvas = Canvas(self.table_figure)
        self.table_frame = EmptyFrame(self.table_canvas, self.controller)
        self.table_canvas.config(bg="#BDBDBD")
        myscrollbar = Scrollbar(self.table_figure, orient="vertical", command=self.table_canvas.yview)
        self.table_canvas.configure(yscrollcommand=myscrollbar.set)
        myscrollbar.pack(side="right", fill="y")
        self.table_canvas.pack(expand=True, fill="both")
        self.table_canvas.create_window((0, 0), window=self.table_frame, anchor='nw')
        self.table_frame.bind("<Configure>", self.scroll_config)
        self.table_frame.bind_all("<MouseWheel>", self._on_mousewheel)


    def _on_mousewheel(self, event):
        self.table_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def scroll_config(self, event):
        self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))

    def show(self):
        try:
            layer = int(self.var_cards.get())
            days_of_validity = int(self.var_val_days.get())
            cards_wanted = []
            cards_non_wanted = []
            minimum_games = int(self.var_games.get())
            sort_by = self.var_sort.get()
            file = "./data/cw_battle_deck_6a6.txt"
        except ValueError:
            messagebox.showinfo("Error", "Bad parameter")
            return 1
        self.refresh_frame()
        colors = ["#F4FA58", "#A4A4A4", "#B45F04"] + ["#E6E6E6"] * 97
        cas = time.time()
        table = top_played_cards.run(layer, days_of_validity, cards_wanted, cards_non_wanted, minimum_games, sort_by, file)
        table.sort(key=lambda x: (x[1][sort_by], x[1][0]+x[1][1]))
        if not self.var_sort2.get():
            table.reverse()
        print(time.time()-cas)
        block_width = 465 + (79*layer)
        self.controller.update()
        screen_width = self.controller.winfo_width()
        columns = screen_width // block_width
        print(columns)
        for i in range(min([len(table), 100])):
            deck_block = EmptyFrame(self.table_frame, self.controller)
            deck_block.grid(column=(i%columns), row = (i // columns))
            Label(deck_block, text=(str(i+1)+"."), font=TABLE_HUGE_FONT, borderwidth=2, relief="solid", width=3,
                  height=2, bg=colors[i]).grid(column=0, row=0)
            for j in range(3):
                Label(deck_block, text=table[i][1][j], font=TABLE_HUGE_FONT, borderwidth=2, relief="solid", width=4, height=2).grid(column=j+1, row=0)
            for j in range(layer):
                photo = ImageTk.PhotoImage(self.controller.images[self.controller.cards_file_name[int(table[i][0][j])]])
                label = Label(deck_block, image=photo, bg="black")
                label.image = photo
                label.grid(column=j+4, row=0)
            deck_block.config(pady=2, padx=5, bg="#BDBDBD")
        print(time.time() - cas)
        pass

    def refresh_frame(self):
        self.table_figure.pack_forget()
        self.table_figure = EmptyFrame(self, self.controller)
        self.table_figure.pack(expand=True, fill="both", side="left", anchor=N)
        self.table_canvas = Canvas(self.table_figure)
        self.table_frame = EmptyFrame(self.table_canvas, self.controller)
        self.table_canvas.config(bg="#BDBDBD")
        myscrollbar = Scrollbar(self.table_figure, orient="vertical", command=self.table_canvas.yview)
        self.table_canvas.configure(yscrollcommand=myscrollbar.set)
        myscrollbar.pack(side="right", fill="y")
        self.table_canvas.pack(expand=True, fill="both")
        self.table_canvas.create_window((0, 0), window=self.table_frame, anchor='nw')
        self.table_frame.bind("<Configure>", self.scroll_config)
        self.table_frame.bind_all("<MouseWheel>", self._on_mousewheel)


class EmptyFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

main = App()
main.geometry("1280x720")
#ani = animation.FuncAnimation(f, show, interval=5000)
main.protocol("WM_DELETE_WINDOW", sys.exit)
main.mainloop()

