import asyncio
import random as r

from pokemon import request, compare, i, Poke

class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.team = []
        for p in self.player.team:
            self.team.append(Competant(p, False))
        self.poke = 0
        self.enemy_team = []
        for p in enemy:
            self.enemy_team.append(Competant(p, True))
        self.enemy_index = 0
        print(f"Go {self.team[self.poke].name}!")
        self.battle_loop()

    # battle loop
    def battle_loop(self):
        while True:
            resp = int(i(text=f"what will {self.player.name} do? fight(1)/switch pokemon(2)/flee(3)"))

            # fight
            if resp == 1:
                print(self.poke)
                text = f"what will {self.team[self.poke].name} do?"
                if len(self.team[self.poke].moves) != 0:
                    for m in self.team[self.poke].moves:
                        text += f"{m.name}({self.team[self.poke].moves.index(m)+1})"
                        if self.team[self.poke].moves.index(m)+1 != 4:
                            text += "/"
                else:
                    text += "no moves"
                move_num = int(i(text=text))
                self.team[self.poke].move = self.team[self.poke].moves[move_num-1]
                self.enemy_team[self.enemy_index].move = r.choice(self.enemy_team[self.enemy_index].moves)

                # comparing speed to see who uses move first
                if compare(self.team[self.poke].speed, self.enemy_team[self.enemy_index].speed) != -1:
                    attacker1 = self.team[self.poke]
                    attacker2 = self.enemy_team[self.enemy_index]
                else:
                    attacker1 = self.enemy_team[self.enemy_index]
                    attacker2 = self.team[self.poke]

                dmg = None

                # attacker 1 uses move
                print(f"{attacker1.name} used {attacker1.move.name}")
                # physical type move
                if attacker1.move.damage_class == 1:
                    print(attacker1.move.power)
                    dmg = ((attacker1.lvl/5+2) * attacker1.move.power * (attacker1.attack / attacker2.defense)) / 50 + 2
                    dmg = round(dmg)
                # special type move
                elif attacker1.move.damage_class == 2:
                    dmg = (((attacker1.lvl* 2)/5+2) * attacker1.move.power * (attacker1.sp_attack / attacker2.sp_defense)) / 50 + 2
                    dmg = round(dmg)
                # status type move
                elif attacker1.move.damage_class == 3:
                    # target to whom to apply the status changes
                    target = (attacker1, attacker2)[attacker1.move.target-1]
                    # checking which status to change
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
                # applying damage
                if dmg:
                    attacker2.hp -= dmg
                    print(f"{attacker2.name} lost {dmg} hp!")
                    if attacker2.hp <= 0:
                        attacker2.fainted = True
                        print(f"{attacker2.name} fainted")
                        if attacker2.enemy:
                            alive = []
                            for p in self.enemy_team:
                                if not p.fainted:
                                    alive.append(p)
                            if len(alive) != 0:
                                self.enemy = enemy_team.index(r.choice(alive))
                            else:
                                print("you won!!!")
                                return
                        else:
                            string = ""
                            alive = []
                            for mon in self.team:
                                if not mon.fainted:
                                    if len(alive) != 0:
                                        string += ' | '
                                    string += f"{self.player.team.index(mon)+1}-{mon.name}({mon.lvl})[{mon.hp+mon.attack+mon.defense+mon.sp_attack+mon.sp_defense+mon.speed}]"
                                    alive.append(mon)
                            print(string)
                            if len(alive) != 0:
                                n = int(i(text="choose the pokemon using its number"))
                                self.poke = n-1
                            else:
                                print("all your pokemons fainted. you lost :(")
                                return

                # attacker 2 uses move
                print(f"{attacker2.name} used {attacker2.move.name}")

                if attacker2.move.damage_class == 1:
                    print(attacker1.move.power)
                    dmg = ((attacker2.lvl/5+2) * attacker2.move.power * (attacker2.attack / attacker1.defense)) / 50 + 2
                    dmg = round(dmg)

                elif attacker2.move.damage_class == 2:
                    dmg = (((attacker2.lvl* 2)/5+2) * attacker2.move.power * (attacker2.sp_attack / attacker1.sp_defense)) / 50 + 2
                    dmg = round(dmg)

                elif attacker2.move.damage_class == 3:
                    target = (attacker2, attacker1)[attacker2.move.target-1]
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
                    print(f"{attacker1.name} lost {dmg} hp!")
                    if attacker1.hp <= 0:
                        attacker1.fainted = True
                        print(f"{attacker1.name} fainted")
                        if attacker1.enemy:
                            alive = []
                            for p in self.enemy_team:
                                if not p.fainted:
                                    alive.append(p)
                            if len(alive) != 0:
                                self.enemy = enemy_team.index(r.choice(alive))
                            else:
                                print("you won!!!")
                                return
                        else:
                            string = ""
                            alive = []
                            for mon in self.team:
                                if not mon.fainted:
                                    if len(alive) != 0:
                                        string += ' | '
                                    string += f"{self.player.team.index(mon)+1}-{mon.name}({mon.lvl})[{mon.hp+mon.attack+mon.defense+mon.sp_attack+mon.sp_defense+mon.speed}]"
                                    alive.append(mon)
                            print(string)
                            if len(alive) != 0:
                                n = int(i(text="choose the pokemon using its number"))
                                self.poke = n-1
                            else:
                                print("all your pokemons fainted. you lost :(")
                                return

            # switch pokemon
            if resp == 2:
                string = f"1-{self.team[0].name}({self.team[0].lvl})[{self.team[0].hp+self.team[0].attack+self.team[0].defense+self.team[0].sp_attack+self.team[0].sp_defense+self.team[0].speed}]"
                if len(team) > 1:
                    for mon in self.team[1:]:
                        string += f" | {self.player.team.index(mon)+1}-{mon.name}({mon.lvl})[{mon.hp+mon.attack+mon.defense+mon.sp_attack+mon.sp_defense+mon.speed}]"
                n = int(i(text="choose the pokemon using its number"))
                self.poke = [n-1]

            # using item from bag (will be implemented later)
            #if resp == 3:
            #    self.show_bag()

            # fleeing
            if resp == 3:
                # comparing speed if faster than the other pokemon then you can flee
                if compare(self.team[self.poke].speed, self.enemy_team[self.enemy_index].speed) != -1:
                    print("You fled from the battle!")
                    break
                else:
                    print("You failed to flee")

# Pokemons' temporary class during battle
class Competant:
    def __init__(self, pokemon, enemy):
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
        self.fainted = False
        self.enemy = enemy