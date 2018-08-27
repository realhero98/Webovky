import api_library
from tkinter import *
from tkinter import ttk
from time import time


def print_data(content, file):
    output = open(file, "w")
    data = api_library.import_data("clan", "JP2VPJU")
    players = [x["tag"] for x in data["members"]]
    output.write(content[0][0]+"\n")
    for i in range(len(content[1])):
        output.write(content[1][i])
        if i + 1 != len(content[1]):
            output.write("\t")
    output.write("\n")
    for i in content[1:]:
        if i[0] in players:
            for j in range(len(i)):
                output.write(i[j])
                if j + 1 != len(i):
                    output.write("\t")
            output.write("\n")


def run(file=""):
    def close_window():
        root.destroy()
    root = Tk()
    root.title("Loading")
    root.minsize(250, 100)
    frame = Frame(root, pady=20)
    frame.size()
    frame.pack(fill=None, expand=False)
    Label(frame, text="Importing Clan War Logs").pack()
    Label(frame, text="Please wait..").pack()
    progressbar = ttk.Progressbar(frame, orient=HORIZONTAL, length=200, mode='determinate', maximum=100)
    progressbar.pack()
    Button(root, text="Cancel", command=close_window).pack()

    progressbar.step(5)
    progressbar.update()
    try:
        output = open(file, "r")

        content = output.read().split("\n")
        output.close()
        for i in range(len(content)): content[i] = content[i].split("\t")
    except FileNotFoundError:
        output = open(file, "w+")
        output.close()
        content = [[""],["xxxxxxxxxx"]]

    if content[0][0] != "" and int(content[0][0]) + 3600 > time():
        print("Last update of Clan War Logs before less than hour")
        output.close()
        progressbar.destroy()
        root.destroy()
        return 0

    next_index = len(content[1])

    data = api_library.import_data("clan", "JP2VPJU", "warlog")

    progressbar.step(50)
    progressbar.update()

    for i in data[::-1]:
        print(i["createdDate"])
        try:
            progressbar.step(10)
            progressbar.update()
        except TclError:
            break
        if str(i["createdDate"]) not in content[1]:
            content[1].append(str(i["createdDate"]))
            for participant in i["participants"]:
                find = False
                for line in content:
                    if participant["tag"]  == line[0]:
                        line.append(str(participant['battlesPlayed']) + "<>" + str(participant['wins']) + "<>" + str(participant['cardsEarned']))
                        find = True
                if not find:
                    content.append([participant["tag"]])
                    for k in range(next_index-1):
                        content[-1].append("NNNNNNNN")
                    content[-1].append(str(participant['battlesPlayed']) + "<>" + str(participant['wins'])+ "<>" + str(participant['cardsEarned']))
            for j in content[2:]:
                if j[0] not in [x["tag"] for x in i["participants"]]:
                    j.append("XXXXXXXX")
            next_index += 1
    content[0] = [str(round(time()))]
    print_data(content, file)
    try:
        progressbar.destroy()
        root.destroy()
    except TclError:
        print("chyba")
        pass
