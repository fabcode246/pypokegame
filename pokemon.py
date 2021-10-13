import aiohttp
import asyncio
import random as r
import json

moves_list = []
with open("pokemons.json", "r") as f:
    moves_list = json.load(f)["moves"]

# a func to compare
def compare(a, b):
    return (a > b) - (a < b)

# func to get input
def i(q=False, text=None):
    if text:
        resp = input("{}: ".format(text))
    elif q:
        resp = input("answer: ")
    else:
        resp = input("type: ")
    return resp

# http requests function
async def request(req):
    link = "https://pokeapi.co/api/v2/{}".format(req)
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            return await response.json()

# a class to get pokemon and all
class Poke:
    def __init__(self):
        self.pokemons = asyncio.run(request("pokemon?limit=2000"))["results"]

    # gets a pokemon using name or pokedex id
    def get(self, name=None, dex=None):
        name = name.lower()
        if name:
            usable = name
        elif dex:
            usable = dex
        data = asyncio.run(request("pokemon/{}".format(usable)))
        return Pokemon(data)

    # to get a wild pokemon
    def get_rand_mon(self, steps):
        wild_mon = r.choice(self.pokemons)
        poke = self.get(name=wild_mon["name"])
        poke.lvl = round(r.uniform(.4, .8) * (steps / 100))
        while len(poke.moves) != 4:
            poke.learn(r.choice(poke.all_moves)['move']['name'], p=False)
        return poke

# Moves of pokemon
class Move:
    def __init__(self, info):
        if info == {}:
            return
        self.name = info['move']["name"]
        self.learned_at = info["version_group_details"][0]["level_learned_at"]
        data = asyncio.run(request(info['move']['url'][26:]))
        damage_class = data["damage_class"]['name']
        self.damage_class = 1 if damage_class == "physical" else 2 if damage_class == "special" else 3
        self.target = 1 if data["target"]['name'] == 'user' else 2
        self.power = data["power"]
        self.max_pp = data["pp"]
        self.pp = data["pp"]
        self.accuracy = data["accuracy"]
        self.id = data['id']
        if len(data['stat_changes']) != 0:
            self.stat_change_amount = data["stat_changes"][0]['change']
            self.stat_change_stat = data["stat_changes"][0]['stat']['name']
        self.type = data["type"]["name"]

# Player Class
class Player:
    def __init__(self, name, starter):
        self.name = name
        self.money = r.randint(1000,1200)
        self.fav = starter
        self.pokemons = [starter,]
        self.team = [starter,]
        self.bag = {"pokeballs": 5, }
        self.steps = 0

# Pokemon Class
class Pokemon:
    global moves_list
    def __init__(self, data):
        self.name = data["name"]
        self.nick = ''
        self.types = []
        for t in data["types"]:
            self.types.append(t['type']['name'])
        all_moves = data["moves"]
        self.all_moves = []
        for m in all_moves:
            self.all_moves.append(m)
        self.moves = []
        stats = self.set_stats(data["stats"])
        self.hp = stats["hp"]
        self.attack = stats["attack"]
        self.defense = stats["defense"]
        self.sp_attack = stats["special-attack"]
        self.sp_defense = stats["special-defense"]
        self.speed = stats["speed"]
        self.base_exp = data['base_experience']
        species = asyncio.run(request(data['species']['url'][26:]))
        self.evo = asyncio.run(request(species['evolution_chain']['url'][26:]))
        self.exp = 0
        self.lvl = 1

    # returns the stats inside a dict
    def set_stats(self, data):
        stats = {}
        for stat in data:
            stats[stat["stat"]["name"]] = stat["base_stat"]
        return stats

    # increment the exp
    def exp(self, amount):
        self.exp += amount
        if self.exp > round(self.level * 1.23 * 15):
            self.level += 1
            self.exp = 0

    # learn a move
    def learn(self, move, p=True):
        found_move = False
        move_data = {}
        for m in self.all_moves:
            if move == m['move']['name']:
                found_move = True
                move_data = m
                break
        if move in moves_list: 
            for m in self.moves:
                if move == m.name:
                    found_move = False
                    break
        else:
            found_move = False
        move_obj = Move(move_data)
        if found_move and move_obj.learned_at <= self.lvl:
            if len(self.moves) == 4:
                if p:
                    print('your pokemon already have four moves')
                yn = i('do you want to replace a move(y/n)')
                if yn in ["yes", "y"]:
                    string = 'moves:'
                    for i in self.moves:
                        string += f' {self.moves.index(i)+1}-{i.name}'
                    if p:
                        print(string)
                    move_index = i('which move to replace')
                    if p:
                        print(f"{self.name} forgot {self.moves[i-1]}")
                    self.moves[i-1] = move_obj
                    if p:
                        print(f"{self.name} learned {move}")
            else:
                self.moves.append(move_obj)
                if p:
                    print(f"{self.name} learned {move}")
        elif move_obj.learned_at > self.lvl:
            if p:
                print('move not learnable yet')
        else:
            if p:
                print('move not found')
