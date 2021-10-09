import aiohttp
import asyncio
import random as r
from time import sleep as s

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

# Moves of pokemon
class Move:
    def __init__(self, info):
        self.name = info["move"]["name"]
        self.learned_at = info["version_group_details"]["level_learned_at"]
        data = asyncio.run(request(info['move']['url'][26:]))
        damage_class = data["damage_class"]['name']
        self.damage_class = 1 if damage_class == "physical" else 2 if damage_class == "special" else 3 if damage_class == "status"
        self.target = 1 if data["target"]['name'] == 'user' else 2
        self.power = data["power"]
        self.max_pp = data["pp"]
        self.pp = data["pp"]
        self.accuracy = data["accuracy"]
        self.id = data[id]
        self.stat_change_amount = data["stat_changes"]['change']
        self.stat_change_stat = data["stat_changes"]['stat']['name']
        self.type = data["type"]["name"]

# Pokemon Class
class Pokemon:
    def __init__(self, data):
        #print(data)
        self.name = data["name"]
        self.nick = ''
        self.types = []
        for t in data["types"]:
            self.types.append(t['type']['name'])
        self.all_moves = data["moves"]
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
        print(self.evo)
        self.exp = 0
        self.lvl = 1

    def set_stats(self, data):
        stats = {}
        for stat in data:
            stats[stat["stat"]["name"]] = stat["base_stat"]
        return stats

    def exp(self, amount):
        self.exp += amount
        if self.exp > round(self.level * 1.23 * 15):
            self.level += 1
            self.exp = 0

    def learn(self, move):
        pass

# a class to get pokemon and all
class Poke:
    def __init__(self):
        self.pokemons = asyncio.run(request("pokemon?limit=2000"))["results"]

    # gets a pokemon using name or pokedex id
    def get(self, name=None, dex=None):
        if name:
            usable = name
        elif dex:
            usable = dex
        data = asyncio.run(request("pokemon/{}".format(usable)))
        return Pokemon(data)

    # to get a wild pokemon
    def get_rand_mon(self):
        wild_mon = r.choice(self.pokemons)
        return self.get(name=wild_mon["name"])

# Player Class
class Player:
    def __init__(self, name, starter):
        self.name = name
        self.money = r.randint(1000,1200)
        self.fav = starter
        self.pokemons = [starter,]
        self.team = [starter,]
        self.bag = {"pokeballs": 5, }

# Pokemons' temporary class during battle
class Competant:
    def __init__(self, pokemon):
        self.name = pokemon.name
        self.types = pokemon.types
        self.moves = pokemon.moves
        self.move = None
        self.hp = pokemon.hp
        self.attack = pokemon.attack
        self.defense = pokemon.defense
        self.sp_attack = pokemon.sp_attack
        self.sp_defense = pokemon.sp_defense
        self.speed = pokemon.speed
        self.lvl = pokemon.lvl

# The class that runs the game
class Game:
    def __init__(self):
        self.start()

    # starts the game
    def start(self):
        print("Hey im professor fern")
        print("what shall i call you?")
        name = i(q=True)
        print("do you want bulbasaur, squirtle, or charmander?")
        starter_name = i(q=True)
        if starter_name == "bulbasaur" or starter_name == "squirtle" or starter_name == "charmander":
            starter = Poke().get(name=starter_name)
            self.player = Player(name, starter)
            print("now type info and get info about your fav pokemon")
            ans = i()
            while ans != "info":
                print("type info")
                ans = i()
            if ans == "info":
                self.info()
                print("good now you can type help to see all the things you can do. Enjoy!!")
                self.loop()

    # the main loop that runs the whole game
    def loop(self):
        runner = True
        while runner:
            command = i()
            # the adventure, 1/3 chance of encountering wild pokemons
            if command == "":
                ns = [1,2,3]
                n = r.choice(ns)
                if n == 1:
                    wild_mon = Poke().get_rand_mon()
                    print(f"A wild {wild_mon.name} appeared!")
                    self.battle(wild_mon)
            elif command in ["h", "help"]:
                text = """HELP
format: command(alias) - description
usage: command {options}
help(h) - shows this
info(i) - shows info bout your fav pokemon
profile(prof) - shows
nothing - travel and maybe meet wild pokemons"""
                print(text)
            elif command in ["info", "i"]:
                self.info()
            elif command in ["profile", "prof"]:
                self.profile()
            elif command in ["quit", "q", "exit"]:
                yn = i(text="are you sure you want to quit?(y/n)")
                if yn == "y" or yn == "yes":
                    break
            else:
                print("unknown command")

    def info(self):
        pokemon = self.player.fav
        lvl = round(((pokemon.exp / round(pokemon.lvl * 1.23 * 15)) * 100) / 5)
        lvlbar = "["
        lvlbar += "+" * lvl
        lvlbar += " " * (20-lvl)
        lvlbar += "]"
        text = f"""#{pokemon.name}({pokemon.nick})
 {lvlbar}
 lvl: {pokemon.lvl}
 exp: {pokemon.exp}
 hp: {pokemon.hp}
 atk: {pokemon.attack}
 def: {pokemon.defense}
 sp-atk: {pokemon.sp_attack}
 sp-def: {pokemon.sp_defense}
 spd: {pokemon.speed}"""
        print(text)

    def profile(self):
        text = f"""PROFILE
 name:{self.player.name}
 fav: {self.player.fav.name}
 pokemons: {len(self.player.pokemons)}"""
        print(text)


    def battle(self, enemy):
        poke = Competant(self.player.fav)
        enemy = Competant(enemy)
        print(f"Go {poke.nick} {poke.name}!")
        while True:
            resp = int(i(text=f"what will {self.player.name} do? fight(1)/switch pokemon(2)/flee(3)"))
            if resp == 1:
                move_num = int(i(text=f"what will {poke.name} do? {poke.moves[0]}(1)/{poke.moves[1]}(2)/{poke.moves[2]}(3)/{poke.moves[3]}(4)"))
                poke.move = poke.moves[move_num]
                enemy.move = r.choice(enemy.moves)
                if compare(poke.speed, enemy.speed) != -1:
                    attacker1 = poke
                    attacker2 = enemy
                else:
                    attacker1 = enemy
                    attacker2 = poke
                print(f"{attacker1.name} used {attacker1.move.name}")
                dmg = None

                if attacker1.move.damage_class == 1:
                    dmg = ((attacker1.lvl/5+2) * attacker1.move.power * (attacker1.attack / attacker2.defense)) / 50 + 2
                elif attacker1.move.damage_class == 2:
                    dmg = (((attacker1.lvl* 2)/5+2) * attacker1.move.power * (attacker1.sp_attack / attacker2.sp_defense)) / 50 + 2
                elif attacker1.move.damage_class == 3:
                    target = (attacker1, attacker2)[attacker1.move.target]
                    if attacker1.move.stat_change_stat == "hp":
                        target.hp += attacker1.move.stat_change_amount
                    if attacker1.move.stat_change_stat == "attack":
                        target.attack += attacker1.move.stat_change_amount
                    if attacker1.move.stat_change_stat == "defense":
                        target.defense += attacker1.move.stat_change_amount
                    if attacker1.move.stat_change_stat == "special-attack":
                        target.sp_attack += attacker1.move.stat_change_amount
                    if attacker1.move.stat_change_stat == "special-defense":
                        target.sp_defense += attacker1.move.stat_change_amount
                    if attacker1.move.stat_change_stat == "speed":
                        target.speed += attacker1.move.stat_change_amount
                if dmg:
                    attacker2.hp -= dmg

                if attacker2.move.damage_class == 1:
                    dmg = ((attacker2.lvl/5+2) * attacker2.move.power * (attacker2.attack / attacker1.defense)) / 50 + 2
                elif attacker2.move.damage_class == 2:
                    dmg = (((attacker2.lvl* 2)/5+2) * attacker2.move.power * (attacker2.sp_attack / attacker1.sp_defense)) / 50 + 2
                elif attacker2.move.damage_class == 3:
                    target = (attacker2, attacker1)[attacker2.move.target]
                    if attacker2.move.stat_change_stat == "hp":
                        target.hp += attacker2.move.stat_change_amount
                    if attacker2.move.stat_change_stat == "attack":
                        target.attack += attacker2.move.stat_change_amount
                    if attacker2.move.stat_change_stat == "defense":
                        target.defense += attacker2.move.stat_change_amount
                    if attacker2.move.stat_change_stat == "special-attack":
                        target.sp_attack += attacker2.move.stat_change_amount
                    if attacker2.move.stat_change_stat == "special-defense":
                        target.sp_defense += attacker2.move.stat_change_amount
                    if attacker2.move.stat_change_stat == "speed":
                        target.speed += attacker2.move.stat_change_amount
                if dmg:
                    attacker1.hp -= dmg
            if resp == 2:
                string = f"1-{self.player.team[0].name}({self.player.team[0].lvl})[{self.player.team[0].hp+self.player.team[0].attack+self.player.team[0].defense+self.player.team[0].sp_attack+self.player.team[0].sp_defense+self.player.team[0].speed}]"
                if len(self.player.team) > 1:
                    for mon in self.player.team[1:]:
                        string += f" | {self.player.team.index(mon)+1}-{mon.name}({mon.lvl})[{mon.hp+mon.attack+mon.defense+mon.sp_attack+mon.sp_defense+mon.speed}]"
                n = int(i(text="choose the pokemon using its number"))
                poke = Competant(self.player.team[n-1])
            #if resp == 3:
            #    self.show_bag()
            if resp == 3:
                if compare(poke.speed, enemy.speed) != -1:
                    print("You fled from the battle!")
                    break
                else:
                    print("You failed to flee")

Game()