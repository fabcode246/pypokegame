import aiohttp
import asyncio
import random as r
from time import sleep as s

def compare(a, b):
    return (a > b) - (a < b)

def i(q=False, text=None):
    if text:
        resp = input("{}: ".format(text))
    elif q:
        resp = input("answer: ")
    else:
        resp = input("type: ")
    return resp

async def request(req):
    link = "https://pokeapi.co/api/v2/{}".format(req)
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            return await response.json()

class Pokemon:
    def __init__(self, data):
        self.name = data["name"]
        self.nick = ''
        self.abilities = data["abilities"]
        self.moves = []
        self.held = None
        stats = self.set_stats(data["stats"])
        self.hp = stats["hp"]
        self.attack = stats["attack"]
        self.defense = stats["defense"]
        self.sp_attack = stats["special-attack"]
        self.sp_defense = stats["special-defense"]
        self.speed = stats["speed"]
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

class Poke:
    def __init__(self):
        self.pokemons = asyncio.run(request("pokemon?limit=2000"))["results"]

    def get(self, name=None, dex=None):
        if name:
            usable = name
        elif dex:
            usable = dex
        data = asyncio.run(request("pokemon/{}".format(usable)))
        return Pokemon(data)

    def get_rand_mon(self):
        wild_mon = r.choice(self.pokemons)
        return self.get(name=wild_mon["name"])

class Player:
    def __init__(self, name, starter):
        self.name = name
        self.money = r.randint(1000,1200)
        self.fav = starter
        self.pokemons = [starter,]
        self.team = [starter,]
        self.bag = {"pokeballs": 5, }

class Game:
    def __init__(self):
        self.start()

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

    def loop(self):
        runner = True
        while runner:
            command = i()
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
        poke = self.player.fav
        print(f"Go {poke.nick} {poke.name}!")
        while True:
            resp = int(i(text=f"what will {self.player.name} do? fight(1)/switch pokemon(2)/flee(3)"))
            if resp == 1:
                move = int(i(text=f"what will {poke.name} do? {poke.move1}(1)/{poke.move2}(2)/{poke.move3}(3)/{poke.move1}(4)"))
            if resp == 2:
                string = f"1-{self.player.team[0].name}({self.player.team[0].lvl})[{self.player.team[0].hp+self.player.team[0].attack+self.player.team[0].defense+self.player.team[0].sp_attack+self.player.team[0].sp_defense+self.player.team[0].speed}]"
                if len(self.player.team) > 1:
                    for mon in self.player.team[1:]:
                        string += f" | {self.player.team.index(mon)+1}-{mon.name}({mon.lvl})[{mon.hp+mon.attack+mon.defense+mon.sp_attack+mon.sp_defense+mon.speed}]"
                n = int(i(text="choose the pokemon using its number"))
                poke = self.player.team[n-1]
            #if resp == 3:
            #    self.show_bag()
            if resp == 3:
                if compare(poke.speed, enemy.speed) != -1:
                    print("You fled from the battle!")
                    break

Game()