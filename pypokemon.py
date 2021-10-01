import aiohttp
import asyncio
import random as r
from time import sleep as s

def i(q=False):
    if q:
        resp = input("answer: ")
    else:
        resp = input("type: ")
    return resp

def p(content, r=True):
    if r:
        print(content, end="\r")
    else:
        print(content)

async def request(req):
    link = "https://pokeapi.co/api/v2/{}".format(req)
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            return await response.json()

class Pokemon:
    def __init__(self, data):
        self.name = data["name"]
        self.moves = data["abilities"]
        self.move1 = None
        self.move2 = None
        self.move3 = None
        self.move4 = None
        self.held = None
        #self.stats = data["basestat"]
        self.exp = 0
        self.lvl = 1

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

class Player:
    def __init__(self, name, starter):
        self.name = name,
        self.money = r.randint(1000,1200)
        self.fav = starter
        self.pokemons = [starter,]
        self.team = [starter,]

class Game:
    def __init__(self):
        self.start()

    def start(self):
        p("hey im professor fern")
        s(1)
        p("what shall i call you?", r=False)
        name = i(q=True)
        p("do you want bulbasaur, squirtle, or charmander?", r=False)
        starter_name = i(q=True)
        if starter_name == "bulbasaur" or starter_name == "squirtle" or starter_name == "charmander":
            starter = Poke().get(name=starter_name)
            self.player = Player(name, starter)
            p("now type info and get info about your fav pokemon", r=False)
            ans = i()
            while ans is not "info":
                p("type info", r=False)
            if ans == "info":
                self.info()

    def loop(self):
        runner = True
        while runner:
            command = i()
            if command == "info":
                self.info()

    def info(self):
        self.player.fav

Game()