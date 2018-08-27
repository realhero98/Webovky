import api_library
from tkinter import *
from tkinter import ttk
from time import time

def run(file):
    root = Tk()

    def close_window():
        root.destroy()

    root.title("Loading")
    root.minsize(250, 100)
    frame = Frame(root, pady=20)
    frame.size()
    frame.pack(fill=None, expand=False)
    Label(frame, text="Importing Clan War Decks").pack()
    Label(frame, text="Please wait..").pack()
    progressbar = ttk.Progressbar(frame, orient=HORIZONTAL, length=200, mode='determinate', maximum=100)
    progressbar.pack()
    Button(root, text="Cancel", command=close_window).pack()

    output = open(file, "r")
    line = output.readline()
    if int(line) + 3600 > time() and line != "":
        print("Last update of Clan War Decks before less than hour")
        output.close()
        progressbar.destroy()
        root.destroy()
        return 0

    battles = []
    line = output.readline()
    while line != "":
        #print(line)
        battles.append(line[:10])
        line = output.readline()
    output.close()

    progressbar.step(5)
    progressbar.update()

    data = api_library.import_data("clan", "JP2VPJU")
    output = open(file, "a")
    loading = 0
    length = len(data["members"])
    for i in data['members']:
        try:
            progressbar.step(95 / length)
            progressbar.update()
        except TclError:
            break
        loading += (100/length)
        print(str(round(loading)) + "%")
        player_data = api_library.import_data("player", str(i["tag"]), "battles")
        for j in player_data:
            if j["type"] == "clanWarWarDay" and str(j["utcTime"]) not in battles:
                root.update_idletasks()
                root.update()
                deck_dict = j["team"][0]["deck"]
                deck = []
                output.write(str(j["utcTime"])+" "+str(i["tag"])+" ")
                for k in deck_dict:
                    deck.append(k["name"])
                    output.write(str(k["id"])+" ")
                deck.sort()
                output.write(str(j["winner"])+"\n")
    output.close()

    output = open(file, "r")
    content = output.read()
    date = str(round(time()))
    content = content.split("\n")
    content[0] = date
    output.close()
    output = open(file, "w")
    for i in content:
        if i != "":
            output.write(i+"\n")
    output.close()
    try:
        progressbar.destroy()
        root.destroy()
    except TclError:
        print("chyba")
        pass
