"""
Training Dungeon

Author: Johann Ries
Description:
A short D&D-inspired terminal adventure demonstrating
Python programming concepts and game logic.
"""

# Standard library imports
import random
import time


# Constants
MIN_TEXT_DELAY = 1
MAX_TEXT_DELAY = 256
DART_TRAP_DC = 12
DART_DAMAGE = 2

# Global variables
Initiative_order = []  # List of creatures and their initiative totals.


# Classes

class Player:
    """Keep track of the player's starting attributes, health, and actions."""

    def __init__(self, character_class):
        self.character_class = character_class

        # Class sets the starting attributes. These values may be balanced later.
        if character_class == "Fighter":
            self.strength = 15
            self.dexterity = 10
            self.constitution = 14
            self.intelligence = 8
            self.wisdom = 10
            self.charisma = 10
            self.maximum_hp = 14
            self.armour = 14
            self.damage = 1 #use of a lights sword, which is a simple melee weapon.
        elif character_class == "Rogue":
            self.strength = 10
            self.dexterity = 15
            self.constitution = 10
            self.intelligence = 12
            self.wisdom = 12
            self.charisma = 10
            self.maximum_hp = 10
            self.armour = 12
            self.damage = 1 #use of a dagger, which is a simple melee weapon.
        elif character_class == "Wizard":
            self.strength = 8
            self.dexterity = 10
            self.constitution = 10
            self.intelligence = 15
            self.wisdom = 13
            self.charisma = 10
            self.maximum_hp = 8
            self.armour = 10
            self.damage = 1 #use of a staff, which is a simple melee weapon. 
        else:
            raise ValueError("Choose Fighter, Rogue, or Wizard.")

        self.current_hp = self.maximum_hp
        self.steps = 0

        
class Enemy:
    """Keep track of an enemy's attributes and health."""

    def __init__(self, creature_type):
        if creature_type == "Bat":
            self.name = "Bat"
            self.strength = 2
            self.dexterity = 15
            self.constitution = 8
            self.intelligence = 2
            self.wisdom = 12
            self.charisma = 4
            self.maximum_hp = 1
            self.armour = 12
            self.attack_modifier = 0
            self.damage = 1
        else:
            raise ValueError("Choose a valid creature type.")

        self.current_hp = self.maximum_hp      



# Game functions

def choose_class():
    """Ask for a class until the player enters a valid number."""
    print("Choose your class:")
    print("1. Fighter")
    print("2. Rogue")
    print("3. Wizard")

    while True:
        choice = input("> ").strip()

        if choice == "1":
            return Player("Fighter")
        elif choice == "2":
            return Player("Rogue")
        elif choice == "3":
            return Player("Wizard")
        else:
            print("Please enter 1, 2, or 3.")

def corridor_trap(player):
    """Resolve the corridor dart trap."""
    story_print("\nYou feel a stone beneath your boot sink into the floor. ", 100, "character")
    story_print("\nA dart shoots from the wall!", 100, "sentence")
    if ability_check(player.dexterity, DART_TRAP_DC, "Dexterity"):
        story_print("You dodge the dart!", 50, "character")
    else:
        story_print(
            f"The dart hits you! You take {DART_DAMAGE} damage.",
            50,
            "character",
        )
        player.current_hp -= DART_DAMAGE


def enter_room_one(player):
    """Show the first room and carry out one chosen action."""
    story_print("\nRoom 1", 100, "character")
    story_print("The player opens an old door and dusty air fills the corridor.", 100, "character")
    story_print("The corridor is long and dark.", 100, "character")
    print("1. Walk forward")
    print("2. Light a torch")
    print("3. Stop and listen")
    while True:
        choice = input("> ").strip()

        if choice == "1":
            action = "Walk forward"
            roll = random.randint(1, 3)
            if roll == 1:
                story_print("CLICK!", 200, "word")
                story_print("You hear something move inside the wall...", 100, "character")
                corridor_trap(player)
            else:
                story_print("You carefully continue down the corridor.", 200, "word")
                        
        elif choice == "2":
            action = "Light a torch"
            story_print("You light a torch and the corridor is illuminated.", 100, "character")
            roll = random.randint(1, 3)
            if roll == 1:
                story_print("You startled a Bat!", 200, "word")
                story_print("Roll for initiative", 100, "sentence")
                Initiative_tracker(None, 0, 1)  # Clear the initiative order for a new encounter.
                story_pause()
                
                bat = Enemy("Bat")

                player_initiative = roll_initiative(player.dexterity)
                Initiative_tracker(player, player_initiative, 0)
                bat_initiative = roll_initiative(bat.dexterity)
                Initiative_tracker(bat, bat_initiative, 0)

                story_print(f"\n{player.character_class} initiative: {player_initiative}",200, "word")
                story_print(f"{bat.name} initiative: {bat_initiative}",200, "word")

                story_print("\nInitiative order:", 200, "word")
                #lets print the entire initiave order, not just the first creature.
                for index, entry in enumerate(Initiative_order):
                    print(f"{index + 1}. {entry['character'].character_class if isinstance(entry['character'], Player) else entry['character'].name} (Initiative: {entry['totall_initiative']})")
                
                


            else:
                story_print("Revealing blood stained walls.", 100, "character")
                story_print("You carefully continue down the corridor approaching the door.", 100, "character")

        elif choice == "3":
            action = "Stop and listen"
        else:
            print("Please enter 1, 2, or 3.")
            continue

        player.steps += 1
        #print(f"\nYou selected: {action}.") ## desicde if this should be printed or not,it repeats the action taken.
        show_status(player)
        return

# Utility functions

def story_print(text, timer, mode):
    """Display story text at a controlled pace."""
    if timer < MIN_TEXT_DELAY or timer > MAX_TEXT_DELAY:
        raise ValueError("Timer must be between 1 and 256 milliseconds.")

    if mode == "character":
        for character in text:
            print(character, end="", flush=True)
            time.sleep(timer / 1000)
        print()

    elif mode == "word":
        for word in text.split():
            print(word, end=" ", flush=True)
            time.sleep(timer / 1000)
        print()

    elif mode == "sentence":
        print(text)
        time.sleep(timer / 1000)

    else:
        raise ValueError("Mode must be 'character', 'word', or 'sentence'.")

def story_pause():
    """Wait for the player before continuing."""
    input("\n[Press Enter to continue]")

def show_status(player):
    """Print the player's current status on one line."""
    story_print(
        f"Class: {player.character_class} | "
        f"HP: {player.current_hp}/{player.maximum_hp} | "
        f"Armour: {player.armour} | "
        f"Steps: {player.steps}"
    , 50, "word")

def roll_initiative(dexterity):
    """Roll initiative using the creature's Dexterity modifier."""
    roll = random.randint(1, 20)
    modifier = (dexterity - 10) // 2
    total = roll + modifier
    # Note In 5e the maximum initiative can be 63 with no magic items.
    return total

def Initiative_tracker(character, totall_initiative, reset_initiative):
    """Add a creature with flag 0, or clear the turn order with flag 1.

    Highest initiative goes first; ties keep their insertion order.
    """
    if reset_initiative == 1:
        Initiative_order.clear()
    elif reset_initiative == 0:
        Initiative_order.append({
            "character": character,
            "totall_initiative": totall_initiative,
        })
        Initiative_order.sort(
            key=lambda entry: entry["totall_initiative"], reverse=True
        )
    else:
        raise ValueError("reset_initiative must be 0 (add) or 1 (clear).")

    return Initiative_order
    

def show_character_sheet(player):
    """Print all six abilities and the player's health and armour when needed."""
    print(f"\n\n{player.character_class.upper()}")
    print()
    print(f"STR: {player.strength:2}")
    print(f"DEX: {player.dexterity:2}")
    print(f"CON: {player.constitution:2}")
    print(f"INT: {player.intelligence:2}")
    print(f"WIS: {player.wisdom:2}")
    print(f"CHA: {player.charisma:2}")
    print()
    print(f"HP:     {player.current_hp}/{player.maximum_hp}")
    print(f"Armour: {player.armour}")
    print("----------")
    


def ability_check(ability_score, dc, check_name):
    """Roll a D20 with an ability modifier and return whether it meets the DC."""
    roll = random.randint(1, 20)
    modifier = (ability_score - 10) // 2
    total = roll + modifier

    print(f"\n{check_name} Check — DC {dc}\n")
    print(f"D20:      {roll}")
    print(f"Modifier: {modifier:+d}")
    print(f"Total:    {total}\n")

    if total >= dc:
        print("SUCCESS")
        return True
    else:
        print("FAILURE")
        return False



def main():
    """Start the adventure and play the beginning of Room 1."""
    story_print("Welcome to the Adventurer's Guild!", 50, "character")
    story_print("Your training begins here.", 50, "character")

    player = choose_class()
    print()
    show_character_sheet(player)
    story_pause()
    enter_room_one(player)
    story_pause()


if __name__ == "__main__":
    main()
