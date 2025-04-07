
from character import Character
import random

class Hero(Character):
    def __init__(self):
        super().__init__()
        # Extra hero attributes to hold values parsed form existing runs
        # Holds default values in case user is not continuing a run
        self.win_streak = 0
        self.short_name = ""
        print("New hero has been created with combat strength:", self.combat_strength, "and health points:", self.health_points)

    def __del__(self):
        print("The Hero object is being destroyed by the garbage collector")
        super().__del__()

    def hero_attacks(self, monster):
        ascii_image = """
                                @@   @@ 
                                @    @  
                                @   @   
               @@@@@@          @@  @    
            @@       @@        @ @@     
           @%         @     @@@ @       
            @        @@     @@@@@     
               @@@@@        @@       
               @    @@@@                
          @@@ @@                        
       @@     @                         
   @@*       @                          
   @        @@                          
           @@                                                    
         @   @@@@@@@                    
        @            @                  
      @              @                  

  """
        print(ascii_image)
        print("    |    Player's weapon (" + str(self.combat_strength) + ") ---> Monster (" + str(monster.health_points) + ")")
        if self.combat_strength >= monster.health_points:
            monster.health_points = 0
            print("    |    You have killed the monster")
        else:
            monster.health_points -= self.combat_strength
            print("    |    You have reduced the monster's health to:", monster.health_points)
