import random
import os
import platform
from hero import Hero
from monster import Monster
import functions as functions_lab06_solution

print("OS Name:", os.name)
print("Python Version:", platform.python_version())

# Define lists
weapons = ["Fist", "Knife", "Club", "Gun", "Bomb", "Nuclear Bomb"]
loot_options = ["Health Potion", "Poison Potion", "Secret Note", "Leather Boots", "Flimsy Gloves"]
belt = []
monster_powers = {"Fire Magic": 2, "Freeze Time": 4, "Super Hearing": 6}

# Create Hero and Monster objects
hero = Hero()
monster = Monster()

# --- Hero Persistence Feature ---
# Prompt user to continue or start a new run
continue_choice = input("Do you want to continue from your previous winning run? (y/n): ").lower().strip()
if continue_choice == "y":
    # If continuing, ask for the hero name for looking up in the save file
    hero_name_input = input("Enter your Hero's name (two words) for persistence lookup: ").strip()
    parts = hero_name_input.split()
    if len(parts) == 2:
        # Create a short name from the first two letters of the first and last name, to match styling in saves
        short_name = parts[0][:2] + parts[1][:1]
    else:
        # If the name format is invalid, set a default short name
        short_name = "AaA"
        print("Invalid name format, using default short name 'AaA'.")
    # Calls the load_hero_state function to check if the hero can continue
    saved_state = functions_lab06_solution.load_hero_state(short_name)
    if saved_state:
        # Update hero stats with pulled values and assign short_name
        hero.health_points, hero.combat_strength, hero.win_streak = saved_state
        hero.short_name = short_name
        print(f"Continuing run for hero {hero.short_name} with {hero.health_points} HP, {hero.combat_strength} strength.")
        # Increase hero's health points based on win streak (as their health will likely be low carrying over from previous runs)
        hero.health_points += (hero.win_streak * 2)
        print(f"Healing hero based on current win streak: {hero.win_streak} (multiplied by 2).")
        print(f"Updated health: {hero.health_points}")
        # Scale monster according to hero's win streak
        monster.combat_strength += hero.win_streak
        monster.health_points += hero.win_streak
        print(f"Monster scaled to {monster.combat_strength} base combat strength and {monster.health_points} base health points due to hero win streak.")
    else:
        # If no valid state is found (hero is not found or is dead), inform the player and start a new run
        print("No valid winning run found for that hero. Starting a new run.")
        hero.win_streak = 0
else:
    if continue_choice != "n":
        # Simple warning if user enters something other than 'y' or 'n'
        print("Invalid entry. Defaulting to no.")
    print("Starting a new run.")
    hero.win_streak = 0

# If hero's short name wasn't set via persistence, prompt for it now.
if hero.short_name == "":
    tries = 0
    # Limit the number of tries to 5, after which a default name is assigned, to speed up game flow
    while tries < 5:
        hero_name = input("Enter your Hero's name (two words): ").strip()
        parts = hero_name.split()
        if len(parts) == 2 and all(part.isalpha() for part in parts):
            hero.short_name = parts[0][:2] + parts[1][:1]
            # Check if the short name is already taken
            # If the name is already taken, prompt for a different one
            if functions_lab06_solution.name_check(hero.short_name) == True:
                print("Hero with that shortened name is still alive. Please choose a different name.")
                continue
            print("Hero nickname set to:", hero.short_name)
            break
        else:
            print("Invalid name. Try again.")
            tries += 1
            if tries > 4:
                print("Too many tries. Using default short name: 'AaA'")
                hero.short_name = "AaA"

# Weapon roll
input("Roll the dice for your weapon (Press enter)")
weapon_roll = random.randint(1, 6)
hero.combat_strength += weapon_roll
print("    |    Hero's weapon:", weapons[weapon_roll - 1], "[+" + str(weapon_roll) + "]")
print("    |    Hero's combat strength increased to:", hero.combat_strength)

# Collect loot
input("Loot roll 1 (Press enter)")
loot_options, belt = functions_lab06_solution.collect_loot(loot_options, belt)
input("Loot roll 2 (Press enter)")
loot_options, belt = functions_lab06_solution.collect_loot(loot_options, belt)
belt.sort()
print("Belt:", belt)

belt, hero.health_points = functions_lab06_solution.use_loot(belt, hero.health_points)

# Dream level validation using try-except
num_dream_lvls = -1
while True:
    try:
        num_dream_lvls = int(input("Enter dream level (0-3): "))
        if 0 <= num_dream_lvls <= 3:
            # Check if the number of dream levels is less than or equal to hero's health points
            # This is to ensure the hero has enough health points to enter that many dream levels (as you lose health based on the number of dream levels)
            if num_dream_lvls >= hero.health_points:
                print("You don't have enough health points to enter that many dream levels.")
                continue
            break
        else:
            print("Number must be between 0 and 3")
    except ValueError:
        print("Please enter a valid integer")

if num_dream_lvls > 0:
    hero.health_points -= num_dream_lvls
    crazy_level = functions_lab06_solution.inception_dream(num_dream_lvls)
    hero.combat_strength += crazy_level
    print("Your combat strength increased by " + str(crazy_level) + ", bringing your total to " + str(hero.combat_strength))
    print(f"Your health points decreased by {num_dream_lvls}, bringing your total to " + str(hero.health_points))

# Power roll
input("Roll for Monster Magic Power (Press enter)")
power = random.choice(list(monster_powers.keys()))
monster.combat_strength += monster_powers[power]
print("Monster combat strength boosted with:", power)
print("Monster's combat strength is now: ", monster.combat_strength)

# Fight loop
while hero.health_points > 0 and monster.health_points > 0:
    input("Roll to see who strikes first (Press enter)")
    roll = random.randint(1, 6)
    if roll % 2 != 0:
        input(f"Hero {hero.short_name} attacks! (Press enter)")
        hero.hero_attacks(monster)
        if monster.health_points > 0:
            input("Monster counter-attacks! (Press enter)")
            monster.monster_attacks(hero)
    else:
        input("Monster attacks! (Press enter)")
        monster.monster_attacks(hero)
        if hero.health_points > 0:
            input("Hero counter-attacks! (Press enter)")
            hero.hero_attacks(monster)

# Determine winner and assign stars
winner = "Hero" if monster.health_points == 0 else "Monster"
functions_lab06_solution.save_game(winner, hero)