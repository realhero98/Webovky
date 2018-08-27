import api_library

def is_in_clan(tag, data):
    pass

def run():
    data = api_library.import_data("clan", "JP2VPJU")
    input = open("./cw_battle_res", "r")
    content = [input.readline()]
    content.append(input.readline().split("\t"))
    input.close()


run()