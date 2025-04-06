
from character import Character
import random

class Monster(Character):
    def __init__(self):
        super().__init__()  
        print("Monster created with combat strength:", self.combat_strength, "and health points:", self.health_points)

    def __del__(self):
        print("The Monster object is being destroyed by the garbage collector")
        super().__del__()

    def monster_attacks(self, hero):
        print("    |    Monster's Claw (" + str(self.combat_strength) + ") ---> Player (" + str(hero.health_points) + ")")
        if self.combat_strength >= hero.health_points:
            hero.health_points = 0
            print("    |    Player is dead")
        else:
            hero.health_points -= self.combat_strength
            print("    |    The monster has reduced Player's health to:", hero.health_points)
