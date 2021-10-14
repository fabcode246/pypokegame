import asyncio
import random as r

from pokemon import request, compare, i, Poke, Player
from extra_classes import Battle

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
            raw_command = i()
            command = raw_command.split()
            # the adventure, 1/3 chance of encountering wild pokemons
            if raw_command == "":
                self.player.steps += 1
                ns = [1,2,3]
                n = r.choice(ns)
                if n == 1:
                    # wild pokemon spawning
                    wild_mon = Poke().get_rand_mon(self.player.steps)
                    print(f"A wild {wild_mon.name} appeared!")
                    Battle(self.player, [wild_mon])
            elif command[0] in ["h", "help"]:
                text = """HELP
format: command(alias) - description
usage: command {options}
help(h) - shows this
info(i) - shows info bout your fav pokemon
profile(prof) - shows
nothing - travel and maybe meet wild pokemons"""
                print(text)
            elif command[0] in ["info", "i"]:
                self.info()
            elif command[0] in ["profile", "prof"]:
                self.profile()
            elif command[0] in ["learn"]:
                if len(command) != 0:
                    self.player.fav.learn(command[1])
            elif command[0] in ["quit", "q", "exit"]:
                yn = i(text="are you sure you want to quit?(y/n)")
                if yn == "y" or yn == "yes":
                    break
            else:
                print("unknown command")

    # shows info of the favorite pokemon of the user
    def info(self):
        pokemon = self.player.fav
        lvl = round(((pokemon.exp / round(pokemon.lvl * 1.23 * 15)) * 100) / 5)
        lvlbar = "["
        lvlbar += "+" * lvl
        lvlbar += " " * (20-lvl)
        lvlbar += "]"
        text = f"""
#{pokemon.name}({pokemon.nick})
 {lvlbar}
 lvl: {pokemon.lvl}
 exp: {pokemon.exp}
 hp: {pokemon.hp}
 atk: {pokemon.attack}
 def: {pokemon.defense}
 sp-atk: {pokemon.sp_attack}
 sp-def: {pokemon.sp_defense}
 spd: {pokemon.speed}
 moves:"""
        if len(pokemon.moves) != 0:
            for i in pokemon.moves:
                text += f"\n  {pokemon.moves.index(i)+1} {i.name}"
        else:
            text += "\n  no moves"
        print(text)

    # shows the profile of the player
    def profile(self):
        text = f"""PROFILE
 name:{self.player.name}
 fav: {self.player.fav.name}
 pokemons: {len(self.player.pokemons)}"""
        print(text)

Game()