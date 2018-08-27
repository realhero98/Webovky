import api_library
import time as ti
def run(LAYER, DAYS_OF_VALIDITY, CARD_WANTED, card_non_wanted, minimum, sort_by, file):
    cards = api_library.get_cards()
    table = {}
    #api_library.make_dict()




    name = {26000046: 'Bandit', 27000003: 'Inferno Tower', 28000004: 'Goblin Barrel', 26000024: 'Royal Giant', 26000002: 'Goblins', 26000044: 'Hunter', 26000006: 'Balloon', 28000009: 'Poison', 26000039: 'Mega Minion', 27000004: 'Bomb Tower', 26000019: 'Spear Goblins', 26000035: 'Lumberjack', 28000011: 'The Log', 26000053: 'Rascals', 28000001: 'Arrows', 27000007: 'Elixir Collector', 26000041: 'Goblin Gang', 26000049: 'Bats', 26000012: 'Skeleton Army', 28000006: 'Mirror', 26000001: 'Archers', 27000005: 'Barbarian Hut', 26000055: 'Mega Knight', 26000030: 'Ice Spirit', 26000036: 'Battle Ram', 26000056: 'Skeleton Barrel', 26000013: 'Bomber', 26000025: 'Guards', 26000032: 'Miner', 28000015: 'Barbarian Barrel', 26000050: 'Royal Ghost', 26000010: 'Skeletons', 26000027: 'Dark Prince', 26000042: 'Electro Wizard', 26000011: 'Valkyrie', 27000008: 'X-Bow', 28000005: 'Freeze', 26000026: 'Princess', 27000010: 'Furnace', 26000052: 'Zappies', 26000022: 'Minion Horde', 28000016: 'Heal', 26000017: 'Wizard', 26000028: 'Three Musketeers', 27000006: 'Tesla', 28000013: 'Clone', 26000016: 'Prince', 26000008: 'Barbarians', 26000037: 'Inferno Dragon', 26000004: 'P.E.K.K.A', 26000029: 'Lava Hound', 26000007: 'Witch', 28000003: 'Rocket', 26000048: 'Night Witch', 26000040: 'Dart Goblin', 28000012: 'Tornado', 26000018: 'Mini P.E.K.K.A', 26000023: 'Ice Wizard', 26000009: 'Golem', 27000000: 'Cannon', 27000009: 'Tombstone', 26000020: 'Giant Skeleton', 26000057: 'Flying Machine', 27000002: 'Mortar', 28000010: 'Graveyard', 26000045: 'Executioner', 26000062: 'Magic Archer', 28000002: 'Rage', 26000034: 'Bowler', 28000007: 'Lightning', 26000043: 'Elite Barbarians', 26000031: 'Fire Spirits', 28000008: 'Zap', 26000038: 'Ice Golem', 26000054: 'Cannon Cart', 26000033: 'Sparky', 26000059: 'Royal Hogs', 28000017: 'Giant Snowball', 26000000: 'Knight', 26000021: 'Hog Rider', 26000005: 'Minions', 27000001: 'Goblin Hut', 28000000: 'Fireball', 26000003: 'Giant', 26000014: 'Musketeer', 26000015: 'Baby Dragon'}

    count = 0
    output = open(file, "r")
    line=output.readline()
    date = round(ti.time())
    line = output.readline()
    while line != "":
        deck_data = line.split(" ")
        if date - (DAYS_OF_VALIDITY * 86400) < int(deck_data[0]):
            leave = False
            deck_names = []
            for i in range(2, 10):
                deck_names.append(deck_data[i])
            for i in CARD_WANTED:
                if i not in deck_names:
                    leave = True
            for i in card_non_wanted:
                if i in deck_names:
                    leave = True
            deck_names.sort()
            if not leave:
                #print(deck_names, deck_data[10][0])
                count += 1
                api_library.procces_deck(table, deck_names, deck_data[10][0], LAYER)
        line = output.readline()

    output.close()

    res = []
    api_library.print_top_played_cards(table, LAYER, res, minimum)

    """j = 0
    for i in res:
        print(i[0]+" = "+str(i[1]))
        j += 1
    print("Vyhovujících balíků: "+str(count)+"\n"+"Kombinaci: "+str(j))
    output = open("top_synergy.txt", "w")
    for i in res:
        output.write(i[0]+"=")
        for j in range(3):
            output.write(" "+str(i[1][j]))
        output.write("\n")

    output.close()"""
    return res
file = "./data/cw_battle_deck_6a6.txt"
layer = 2
days_of_validity = 7
cards_wanted = []
cards_non_wanted = []
minimum_games = 7
sort_by = 2   #sort by 0 wins 1 lost 2 percentage

"""
Success is calculate from games where the cards wanted was used
"""
#run(layer, days_of_validity, cards_wanted, cards_non_wanted, minimum_games, sort_by, file)