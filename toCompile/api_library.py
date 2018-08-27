import requests
from random import randint
from copy import deepcopy


def import_data(issue, tag="", bonus=""):
    if tag != "":
        url = "https://api.royaleapi.com/"+issue+"/"+tag+"/"+bonus
    else:
        url = "https://api.royaleapi.com/" + issue + "/"

    headers = {
        'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6OTA4LCJpZGVuIjoiNDU3NjExNDE5MTI3MzgyMDQ5IiwibWQiOnt9LCJ0cyI6MTUyOTE4MjE1NDM0OH0.hva9_kQgCq6stmGnQd_lAomDojYdfzko94QUkVPcS_g"
    }

    response = requests.request("GET", url, headers=headers)

    data = response.json()
    return data

def get_cards():
    cards = []
    data = import_data("player", "8RPGV992")
    for i in data["cards"]:
        cards.append(i["name"])
    return sorted(cards)

def make_table(cards):              #nonUsed
    table = {}
    for i in range(len(cards)-2):
        table[cards[i]] = {}
    return table

def procces_deck(table, deck, result, layer):
    if layer > 1:
        for i in range(len(deck)-layer+1):
            if deck[i] not in table:
                table[deck[i]] = {}
            procces_deck(table[deck[i]], deck[i+1:], result, layer - 1)
    else:
        for i in deck:
            if i not in table:
                table[i] = [0, 0]
            if result == "1" or result == "2" or result == "3":
                table[i][0] += 1
            else:
                table[i][1] += 1

"""def getNameOfCard(id):
    name = {26000046: 'Bandit', 27000003: 'Inferno Tower', 28000004: 'Goblin Barrel', 26000024: 'Royal Giant',
            26000002: 'Goblins', 26000044: 'Hunter', 26000006: 'Balloon', 28000009: 'Poison', 26000039: 'Mega Minion',
            27000004: 'Bomb Tower', 26000019: 'Spear Goblins', 26000035: 'Lumberjack', 28000011: 'The Log',
            26000053: 'Rascals', 28000001: 'Arrows', 27000007: 'Elixir Collector', 26000041: 'Goblin Gang',
            26000049: 'Bats', 26000012: 'Skeleton Army', 28000006: 'Mirror', 26000001: 'Archers',
            27000005: 'Barbarian Hut', 26000055: 'Mega Knight', 26000030: 'Ice Spirit', 26000036: 'Battle Ram',
            26000056: 'Skeleton Barrel', 26000013: 'Bomber', 26000025: 'Guards', 26000032: 'Miner',
            28000015: 'Barbarian Barrel', 26000050: 'Royal Ghost', 26000010: 'Skeletons', 26000027: 'Dark Prince',
            26000042: 'Electro Wizard', 26000011: 'Valkyrie', 27000008: 'X-Bow', 28000005: 'Freeze',
            26000026: 'Princess', 27000010: 'Furnace', 26000052: 'Zappies', 26000022: 'Minion Horde', 28000016: 'Heal',
            26000017: 'Wizard', 26000028: 'Three Musketeers', 27000006: 'Tesla', 28000013: 'Clone', 26000016: 'Prince',
            26000008: 'Barbarians', 26000037: 'Inferno Dragon', 26000004: 'P.E.K.K.A', 26000029: 'Lava Hound',
            26000007: 'Witch', 28000003: 'Rocket', 26000048: 'Night Witch', 26000040: 'Dart Goblin',
            28000012: 'Tornado', 26000018: 'Mini P.E.K.K.A', 26000023: 'Ice Wizard', 26000009: 'Golem',
            27000000: 'Cannon', 27000009: 'Tombstone', 26000020: 'Giant Skeleton', 26000057: 'Flying Machine',
            27000002: 'Mortar', 28000010: 'Graveyard', 26000045: 'Executioner', 26000062: 'Magic Archer',
            28000002: 'Rage', 26000034: 'Bowler', 28000007: 'Lightning', 26000043: 'Elite Barbarians',
            26000031: 'Fire Spirits', 28000008: 'Zap', 26000038: 'Ice Golem', 26000054: 'Cannon Cart',
            26000033: 'Sparky', 26000059: 'Royal Hogs', 28000017: 'Giant Snowball', 26000000: 'Knight',
            26000021: 'Hog Rider', 26000005: 'Minions', 27000001: 'Goblin Hut', 28000000: 'Fireball', 26000003: 'Giant',
            26000014: 'Musketeer', 26000015: 'Baby Dragon'}
    print([name.get(x) for x in name])
    return name[id]
    pass"""

def getNameOfCardFile(id):
    name = {26000046: 'bandit', 27000003: 'inferno-tower', 28000004: 'goblin-barrel', 26000024: 'royal-giant',
            26000002: 'goblins', 26000044: 'hunter', 26000006: 'balloon', 28000009: 'poison', 26000039: 'mega-minion',
            27000004: 'bomb-tower', 26000019: 'spear-goblins', 26000035: 'lumberjack', 28000011: 'the-log',
            26000053: 'rascals', 28000001: 'arrows', 27000007: 'elixir-collector', 26000041: 'goblin-gang',
            26000049: 'bats', 26000012: 'skeleton-army', 28000006: 'mirror', 26000001: 'archers',
            27000005: 'barbarian-hut', 26000055: 'mega-knight', 26000030: 'ice-spirit', 26000036: 'battle-ram',
            26000056: 'skeleton-barrel', 26000013: 'bomber', 26000025: 'guards', 26000032: 'miner',
            28000015: 'barbarian-barrel', 26000050: 'royal-ghost', 26000010: 'skeletons', 26000027: 'dark-prince',
            26000042: 'electro-wizard', 26000011: 'valkyrie', 27000008: 'x-bow', 28000005: 'freeze',
            26000026: 'princess', 27000010: 'furnace', 26000052: 'zappies', 26000022: 'minion-horde', 28000016: 'heal',
            26000017: 'wizard', 26000028: 'three-musketeers', 27000006: 'tesla', 28000013: 'clone', 26000016: 'prince',
            26000008: 'barbarians', 26000037: 'inferno-dragon', 26000004: 'pekka', 26000029: 'lava-hound',
            26000007: 'witch', 28000003: 'rocket', 26000048: 'night-witch', 26000040: 'dart-goblin',
            28000012: 'tornado', 26000018: 'mini-pekka', 26000023: 'ice-wizard', 26000009: 'golem',
            27000000: 'cannon', 27000009: 'tombstone', 26000020: 'giant-skeleton', 26000057: 'flying-machine',
            27000002: 'mortar', 28000010: 'graveyard', 26000045: 'executioner', 26000062: 'magic-archer',
            28000002: 'rage', 26000034: 'bowler', 28000007: 'lightning', 26000043: 'elite-barbarians',
            26000031: 'fire-spirits', 28000008: 'zap', 26000038: 'ice-golem', 26000054: 'cannon-cart',
            26000033: 'sparky', 26000059: 'royal-hogs', 28000017: 'giant-snowball', 26000000: 'knight',
            26000021: 'hog-rider', 26000005: 'minions', 27000001: 'goblin-hut', 28000000: 'fireball', 26000003: 'giant',
            26000014: 'musketeer', 26000015: 'baby-dragon'}
    return name[id]
    pass

def make_dict():
    cards = {}
    data = import_data("player", "8RPGV992")
    for i in data["cards"]:
        cards[i["id"]] = i["name"]
    print(cards)
    pass

def print_top_played_cards(table, layer, res, minimum, start = True, tmp = []):
    if layer > 1:
        for i in table:
            if table[i] != {}:
                tmp2 = deepcopy(tmp)
                tmp2.append(i)
                print_top_played_cards(table[i], layer - 1, res, minimum, False, tmp2)
    else:
        for i in table:
            table[i].append(round(table[i][0]/(table[i][0]+table[i][1]),2))
            if start and table[i][0]+table[i][1] >= minimum:
                res.append([[i], table[i]])
            elif start:
                pass
            else:
                tmp2 = deepcopy(tmp)
                tmp2.append(i)
                if table[i][0]+table[i][1] > minimum:
                    res.append([tmp2, table[i]])

def process_in_row(y_list, line, type):
    y = 0
    type = 3
    if type == 1:
        for index in range(1, len(line)):
            if "<>" in line[index]:
                status = line[index].split("<>")
                y += int(status[1])
                if status[1] != status[0]:
                    y = 0
            y_list.append(y)
    if type == 2:
        for index in range(1, len(line)):
            if "<>" in line[index]:
                status = line[index].split("<>")
                y += int(status[0]) - int(status[1])
                if int(status[0]) == int(status[1]):
                    y = 0
            y_list.append(y)
    if type == 3:
        for index in range(1, len(line)):
            if "<>" in line[index]:
                status = line[index].split("<>")
                if y < 0:
                    y -= int(status[0]) - int(status[1])
                    if int(status[0]) == 0:
                        y -= 1
                    elif int(status[0]) == int(status[1]):
                        y = int(status[1])
                elif y > 0:
                    y += int(status[1])
                    if status[1] != status[0] or int(status[0]) == 0:
                        y = -1
                else:
                    if status[0] == status[1] and int(status[0]) != 0:
                        y += int(status[1])
                    elif int(status[0]) == 0:
                        y = -1
                    else:
                        y -= int(status[0]) - int(status[1])
            y_list.append(y)

def member_dict():
    data = import_data("clan", "JP2VPJU")
    dict = {}

    tmp = open("./sources/colors.txt", "r")
    content = tmp.read().split("\t")
    content = ["#"+x for x in content]

    for member in data["members"]:
        dict[member["tag"]] = [member["name"], content.pop(randint(0, len(content)))]
    return dict