# Import the random library to use for the dice later
import random

# Will the line below print when you import function.py into main.py?
# print("Inside function.py")


def use_loot(belt, health_points):
    good_loot_options = ["Health Potion", "Leather Boots"]
    bad_loot_options = ["Poison Potion"]

    print("    |    !!You see a monster in the distance! So you quickly use your first item:")
    first_item = belt.pop(0)
    if first_item in good_loot_options:
        health_points = min(20, (health_points + 2))
        print("    |    You used " + first_item + " to up your health to " + str(health_points))
    elif first_item in bad_loot_options:
        health_points = max(0, (health_points - 2))
        print("    |    You used " + first_item + " which hurt your health to " + str(health_points))
    else:
        print("    |    You used " + first_item + " but it's not helpful")
    return belt, health_points


def collect_loot(loot_options, belt):
    ascii_image3 = """
                      @@@ @@                
             *# ,        @              
           @           @                
                @@@@@@@@                
               @   @ @% @*              
            @     @   ,    &@           
          @                   @         
         @                     @        
        @                       @       
        @                       @       
        @*                     @        
          @                  @@         
              @@@@@@@@@@@@          
              """
    print(ascii_image3)
    loot_roll = random.choice(range(1, len(loot_options) + 1))
    loot = loot_options.pop(loot_roll - 1)
    belt.append(loot)
    print("    |    Your belt: ", belt)
    return loot_options, belt

# Recursion
# You can choose to go crazy, but it will reduce your health points by the number of dream levels
def inception_dream(num_dream_lvls):
    num_dream_lvls = int(num_dream_lvls)
    # Base Case
    if num_dream_lvls == 1:
        print("    |    You are in the deepest dream level now")
        print("    |", end="    ")
        input("Start to go back to real life? (Press Enter)")
        print("    |    You start to regress back through your dreams to real life.")
        return 2

    # Recursive Case
    else:
        # inception_dream(5)
        # 1 + inception_dream(4)
        # 1 + 1 + inception_dream(3)
        # 1 + 1 + 1 + inception_dream(2)
        # 1 + 1 + 1 + 1 + inception_dream(1)
        # 1 + 1 + 1 + 1 + 2
        return 1 + int(inception_dream(num_dream_lvls - 1))

def load_hero_state(short_name):
    try:
        with open("save.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        return None

    # Filter for all lines that match the provided short name
    matching_lines = [line.strip() for line in lines if line.startswith(f"Hero {short_name}")]
    # If no matching lines, exits the function
    if not matching_lines:
        return None
    # Find the last record for the hero
    # If the last record contains "lost", the hero cannot continue
    last_record = matching_lines[-1].strip()
    if "lost" in last_record:
        print("The requested hero died on their most recent adventure. Cannot continue.")
        return None
    # Expected format provided by save function: "Hero {short_name} | Health: {health_points} | Strength: {combat_strength} | WinStreak: {win_streak}"
    try:
        # If the last record for a hero is not a loss, parse the health points, combat strength, and win streak
        parts = last_record.split("|")
        health_part = parts[1].strip()      # "Health: {health_points}"
        strength_part = parts[2].strip()    # "Strength: {combat_strength}"
        winstreak_part = parts[3].strip()   # "WinStreak: {win_streak}"
        health_points = int(health_part.split(":")[1].strip())
        combat_strength = int(strength_part.split(":")[1].strip())
        win_streak = int(winstreak_part.split(":")[1].strip())
        # Return the parsed values as a tuple
        return (health_points, combat_strength, win_streak)
    except Exception as e:
        # If unable to parse, print an error message and return None
        print("Error parsing saved hero state:", e)
        return None

def save_game(winner, hero, num_stars=0):
    with open("save.txt", "a") as file:
        if winner == "Hero":
            # Increase win streak if one exists, otherwise set to 1.
            if hasattr(hero, "win_streak"):
                hero.win_streak += 1
            else:
                hero.win_streak = 1
            # Save the hero's state on a win, in the expected format.
            file.write(f"Hero {hero.short_name} | Health: {hero.health_points} | Strength: {hero.combat_strength} | WinStreak: {hero.win_streak}\n")
        elif winner == "Monster":
            # Reset win streak upon defeat, then save to file.
            if hasattr(hero, "win_streak"):
                hero.win_streak = 0
            file.write(f"Hero {hero.short_name} lost. WinStreak reset to 0.\n")

def name_check(short_name):
    # Check if an entered name exists in the save file.
    try:
        with open("save.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        return None

    # Filter for lines that are win records for this hero.
    matching_lines = [line.strip() for line in lines if line.startswith(f"Hero {short_name}")]
    # If no matching lines, exits the function (returning false to signify that the name is available)
    if not matching_lines:
        return False
    # Find the last record for the hero
    last_record = matching_lines[-1].strip()
    # If the last record contains "lost", then the name is free
    if "lost" in last_record:
        return False
    # Otherwise, return true to indicate that a hero with that name is still alive (and thus the name is unavailable)
    else:
        return True
