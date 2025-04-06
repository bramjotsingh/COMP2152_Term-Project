
import random

class Character:
    def __init__(self):
        self._combat_strength = random.randint(1, 6)
        self._health_points = random.randint(1, 20)

    def __del__(self):
        print("The Character object is being destroyed by the garbage collector")

    @property  
    def combat_strength(self):
        return self._combat_strength

    @combat_strength.setter
    def combat_strength(self, value):
        if 0 <= value <= 20:
            self._combat_strength = value

    @property
    def health_points(self):
        return self._health_points

    @health_points.setter
    def health_points(self, value):
        if 0 <= value <= 20:
            self._health_points = value
