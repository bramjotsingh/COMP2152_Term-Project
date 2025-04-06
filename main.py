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

# Weapon roll
input("Roll the dice for your weapon (Press enter)")
weapon_roll = random.randint(1, 6)
hero.combat_strength += weapon_roll
print("    |    Hero's weapon:", weapons[weapon_roll - 1])

# Adjust combat strength based on previous game
functions_lab06_solution.adjust_combat_strength(hero.combat_strength, monster.combat_strength)

# Roll for health points
input("Roll for your health points (Press enter)")
hero.health_points = random.randint(1, 20)
print("Hero health:", hero.health_points)

# Check if hero qualifies for the Treasure Room
if hero.health_points > 10 and hero.combat_strength > 3:
    belt = functions_lab06_solution.enter_treasure_room(hero, belt)
else:
    print("\nYou do not qualify to enter the Treasure Room. Stay strong!\n")
input("Roll for monster health points (Press enter)")
monster.health_points = random.randint(1, 20)
print("Monster health:", monster.health_points)

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
            break
        else:
            print("Number must be between 0 and 3")
    except ValueError:
        print("Please enter a valid integer")

if num_dream_lvls > 0:
    hero.health_points -= 1
    crazy_level = functions_lab06_solution.inception_dream(num_dream_lvls)
    hero.combat_strength += crazy_level

# Power roll
input("Roll for Monster Magic Power (Press enter)")
power = random.choice(list(monster_powers.keys()))
monster.combat_strength += monster_powers[power]
print("Monster combat strength boosted with:", power)

# Fight loop
while hero.health_points > 0 and monster.health_points > 0:
    input("Roll to see who strikes first (Press enter)")
    roll = random.randint(1, 6)
    if roll % 2 != 0:
        input("Hero attacks! (Press enter)")
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

# Determine winner
winner = "Hero" if monster.health_points == 0 else "Monster"
num_stars = 3 if winner == "Hero" else 1

# Hero name input
tries = 0
while tries < 5:
    hero_name = input("Enter your Hero's name (two words): ")
    parts = hero_name.split()
    if len(parts) == 2 and all(part.isalpha() for part in parts):
        short_name = parts[0][:2] + parts[1][:1]
        print("Hero nickname:", short_name)
        break
    else:
        print("Invalid name. Try again.")
        tries += 1

# Display stars
print("Hero", short_name, "gets", "*" * num_stars)
functions_lab06_solution.save_game(winner, hero_name=short_name, num_stars=num_stars)

# Write number of monsters killed to file
with open("save.txt", "a") as file:
    if winner == "Hero":
        file.write("Total monsters killed so far: 1\n")
