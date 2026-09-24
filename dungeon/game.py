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
            self.attack_ability = self.strength
            self.stat = "player"
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
            self.attack_ability = self.dexterity
            self.stat = "player"
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
            self.attack_ability = self.intelligence 
            self.stat = "player"
        else:
            raise ValueError("Choose Fighter, Rogue, or Wizard.")

        self.current_hp = self.maximum_hp
        self.steps = 0
        self.inventory = []
        self.skill_check_bonus = 0

        
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
            self.stat = "NPC"
        elif creature_type == "Golomb":
            self.name = "Golomb"
            self.strength = 8
            self.dexterity = 14
            self.constitution = 10
            self.intelligence = 2
            self.wisdom = 10
            self.charisma = 4
            self.maximum_hp = 5
            self.armour = 12
            self.attack_modifier = 2
            self.damage = 1
            self.stat = "NPC"
        elif creature_type == "large_golomb":
            self.name = "large_golomb"
            self.strength = 8
            self.dexterity = 14
            self.constitution = 10
            self.intelligence = 2
            self.wisdom = 10
            self.charisma = 4
            self.maximum_hp = 8
            self.armour = 12
            self.attack_modifier = 2
            self.damage = 1
            self.stat = "NPC"
        else:
            raise ValueError("Choose a valid creature type.")

        self.current_hp = self.maximum_hp      

class Item:
    """Keep track of an item's attributes and effects."""

    def __init__(self, item_type):
        if item_type == "small blue potion":
            self.name = "Small Blue Potion"
            self.effect = "Improves ability check +3."
            self.skill_check_bonus = 3
            self.stat = "item"
        elif item_type == "blue gem":
            self.name = "Blue Gem"
            self.effect = "Unknown"
            self.skill_check_bonus = 0
            self.stat = "item"

        else:
            raise ValueError("Choose a valid item type.")

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
    if ability_check(player, player.dexterity, DART_TRAP_DC, "Dexterity"):
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
                # resolving combat until one side is defeated.
                victor = combat_victor()
                while victor is None:
                    result = combat()
                    if result == "escaped":
                        break
                    victor = combat_victor()

            else:
                story_print("Revealing blood stained walls.", 100, "character")
                story_print("You carefully continue down the corridor approaching the door.", 100, "character")

        elif choice == "3":
            action = "Stop and listen"
            story_print("You stop and listen carefully.", 100, "character")
            roll = random.randint(1, 3)
            if roll == 1:
                story_print("You hear a faint clicking sound as a small Golomb scuttles towards you.", 100, "character")
                story_print("Roll for initiative", 100, "sentence")
                Initiative_tracker(None, 0, 1)  # Clear the initiative order for a new encounter.
                story_pause()
                golomb = Enemy("Golomb")

                player_initiative = roll_initiative(player.dexterity)
                Initiative_tracker(player, player_initiative, 0)
                golomb_initiative = roll_initiative(golomb.dexterity)
                Initiative_tracker(golomb, golomb_initiative, 0)

                story_print(f"\n{player.character_class} initiative: {player_initiative}",200, "word")
                story_print(f"{golomb.name} initiative: {golomb_initiative}",200, "word")

                story_print("\nInitiative order:", 200, "word")
                for index, entry in enumerate(Initiative_order):
                    print(f"{index + 1}. {entry['character'].character_class if isinstance(entry['character'], Player) else entry['character'].name} (Initiative: {entry['totall_initiative']})")
                victor = combat_victor()
                while victor is None:
                    result = combat()
                    if result == "escaped":
                        break
                    victor = combat_victor()
            else:
                story_print("You hear nothing and You carefully continue down the corridor approaching the door.", 100, "character")
               
        else:
            print("Please enter 1, 2, or 3.")
            continue

        player.steps += 1
        #print(f"\nYou selected: {action}.") ## desicde if this should be printed or not,it repeats the action taken.
        show_status(player)
        return

def enter_room_two(player):
    story_print("\nRoom 2", 100, "character")
    story_print("As you approach the second room you are confronted with alrge wooden door. ", 100, "character")
    #if initiative_order is empty then no combat happend, the initiate lock puzzle.
    if not Initiative_order:
        story_print("The door is locked, and you need to solve a puzzle to open it.", 100, "character")
        story_print("you notice three leveres on the locking mechanicsm....A COMBINATION LOCK", 100, "character")
        combination_lock()
        story_print("The door unlocks and you can proceed to the next room.", 100, "character")
        
        story_print("As the door opens slowly you notice a semmingle empty room excep for a small chest in the misddle of the room.", 100, "character")
        
        story_print("please selcte one of the following:", 100, "character")
        story_print("1. inspect the chest\n2. skip ove the chest and continue to the next door", 100, "character")
        while True:
            choice = input("> ").strip()
            if choice == "1":
                story_print("You inspect the chest and discovered it is locked. ", 100, "character")
                story_print("Please select option below", 100, "character")
                story_print("1. Attempt to pick the lock\n2. Break teh lock open \n3. Leave the chest and continue", 100, "character")
                while True:
                    choice = input("> ").strip()
                    if choice == "1":
                        story_print("You attempt to pick the lock.", 100, "character")
                        if ability_check(player, player.dexterity, 12, "Dexterity"):
                            story_print("You successfully pick the lock and open the chest!", 100, "character")
                            story_print("You break the lock open and find a small blue potion.", 100, "character")

                            potion = Item("small blue potion")
                            potion_mechanic(player, potion)
                        else:
                            story_print("You fail to pick the lock and trigger a trap! You take 3 damage.", 100, "character")
                            player.current_hp -= 3
                            story_print(f"Your current HP is now {player.current_hp}/{player.maximum_hp}.", 100, "character")
                        break
                    elif choice == "2":
                        story_print("You break the lock open and find a small blue potion.", 100, "character")
                        story_print("Inside the chest you find a small potion of blue liquid.", 100, "character")

                        potion = Item("small blue potion")
                        potion_mechanic(player, potion)

                        break
                    elif choice == "3":
                        story_print("You leave the chest and continue to the next door.", 100, "character")
                        break
                    else:
                        print("Please enter 1, 2, or 3.")
                
                break
            elif choice == "2":
                story_print("You skip over the chest and continue to the next door.", 100, "character")
                break
            else:
                print("Please enter 1 or 2.")

def enter_room_three(player):
    """Describe the third room's door and ask the player what to do."""
    story_print(
        "As you move beyond the chest, you approach a large wooden door.",
        100,
        "character",
    )
    story_print("The door is six feet tall and has a steel handle and a barred opening "
        "with a sliding cover.",100,"character")
    # the room contains one large golomb regardless of players choice.
    large_golomb = Enemy("large_golomb")

    story_print("What do you intend to do?", 100, "character")
    story_print(
        "1. Open the door.\n2. Slide open the cover over the barred opening.",
        100,
        "character",
    )

    while True:
        choice = input("> ").strip()
        
        if choice == "1":
            story_print("The door opens and you notice a large room with a fountain in the center",100,"character")
            story_print("Behind the fountain you see a door in the distance.",100."character")
            story_print("what do you do?",100, "word")
            story_print("1. approach the fountain\n 2. Examine the room",100, "word")

            while True:
                    choice = input("> ").strip()
                    if choice == "1":
                        story_print("You cautiously approach the fountain.",100,"character")
                        story_print("Beneath the clear water you see it — the Blue Gem.",100,"character")
                        story_print("A heavy metallic footstep echoes behind you.",100, "character")
                        story_print("The mechanical golem turns towards the fountain.",100,"character")
                        story_print("What do you do?\n1. Fight the golem\n2. Attempt to steal the gem\n3. Grab the gem and run",100,"character")
                        while True:
                                            choice = input("> ").strip()
                                            if choice == "1":
                                                story_print("Roll for initiative!",200,"sentence")

                                                player_initiative = roll_initiative(player.dexterity)
                                                Initiative_tracker(player, player_initiative, 0)
                                                golomb_initiative = roll_initiative(large_golomb.dexterity)
                                                Initiative_tracker(large_golomb, golomb_initiative, 0)

                                                story_print(f"\n{player.character_class} initiative: {player_initiative}",200, "word")
                                                story_print(f"{large_golomb.name} initiative: {golomb_initiative}",200, "word")

                                                story_print("\nInitiative order:", 200, "word")
                                                #lets print the entire initiave order, not just the first creature.
                                                for index, entry in enumerate(Initiative_order):
                                                    print(f"{index + 1}. {entry['character'].character_class if isinstance(entry['character'], Player) else entry['character'].name} (Initiative: {entry['totall_initiative']})")
                                                # resolving combat until one side is defeated.
                                                victor = combat_victor()
                                                while victor is None:
                                                    result = combat()
                                                    if result == "escaped":
                                                        break
                                                    victor = combat_victor()
                                            elif choice == "2":
                                                story_print("YOu notice the golomb does not look at the pedastal",100,"character")
                                                story_print("you try to snatch the gem from the fountain with showing you hand to the golumb",100, "charcater")
                                                if ability_check(player, player.dexterity, 13, "Dexterity"):
                                                    story_print("You successfull grab the gem unoticed\nslowly you back away fromthe fountain\navoiding ther golombs action.", 100, "character")
                                                    blue_gem =Item("blue gem")
                                                    player.inventory.append(blue_gem)
                                                else:
                                                    story_print(
                                                        "Your fingers appoach the Blue Gem.",100,"character")
                                                    story_print("CLANK!",200,"word")
                                                    story_print("The golem's head snaps towards you. You have been spotted!",100,"character",)



                    elif choice == "2":
                        story_print(
                            "You slowly slide open the cover and peer through the bars.",
                            100,
                            "character",
                        )
                        story_print(
                            "A large stone chamber lies beyond the door. "
                            "A fountain stands in the centre of the room.",
                            100,
                            "character",
                        )
                        story_print(
                            "Something blue glimmers beneath the water.",
                            100,
                            "character",
                        )
                        story_print(
                            "Near the fountain stands a large mechanical golem. "
                            "It does not appear to have noticed you.",
                            100,
                            "character",
                        )
                     
                        
            break
        elif choice == "2":
            break
        else:
            print("Please enter 1 or 2.")


def potion_mechanic(player, potion_type):
    """Allow the player to drink, store, or leave a potion."""

    story_print("1. drink it now\n2. Keep it for later\n3. Leave it alone", 100, "character")
    while True:
            choice = input("> ").strip()

            if choice == "1":
                story_print("You drink the potion and feel strangely capable!",100,"character")
                player.skill_check_bonus = potion.skill_check_bonus            
                break

            elif choice == "2":
                story_print(
                    "You keep the potion for later.",100,"character")
                player.inventory.append(potion)
                break

            elif choice == "3":
                story_print("You leave the potion alone.",100,"character")
                break

            else:
                print("Please enter 1, 2, or 3.")


def combination_lock():
    """A simple combination binary lock puzzle."""
    story_print("Select a combination of three levers to unlock the door.", mode="character", timer=100)
    story_print("0. [000]\n1. [001]\n2. [010]\n3. [011]\n4. [100]\n5. [101]\n6. [110]\n7. [111]", mode="character", timer=100)
    story_print("An inscription reads: 'Add two and three, then set the levers to that number in binary.'", mode="character", timer=100)
    correct_combination = "5"
    sound_patterns = {
        "0": "CLICK - THUD - CLICK",
        "1": "CLICK - THUD - THUD",
        "2": "CLICK - CLICK - CLICK",
        "3": "CLICK - CLICK - THUD",
        "4": "THUD - THUD - CLICK",
        "5": "THUD - THUD - THUD",
        "6": "THUD - CLICK - CLICK",
        "7": "THUD - CLICK - THUD",
    }
    while True:
        selection = input("Select a number from 0 through 7: ").strip()
        if selection not in sound_patterns:
            print("Please enter a number between 0 and 7.")
            continue

        story_print(sound_patterns[selection], mode="character", timer=100)
        if selection == correct_combination:
            story_print("The mechanism unlocks.", mode="character", timer=100)
            return True

        story_print("The lock remains closed.", mode="character", timer=100)


# Utility functions

def party_inventory():
    """Display the party's inventory."""
    # This function is a placeholder for future inventory management.
    story_print("Inventory management is not yet implemented.", 100, "character")

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

def combat_victor():
    """Check which side still has living combatants."""

    players_alive = False
    npcs_alive = False

    for entry in Initiative_order:
        character = entry["character"]

        if character.current_hp > 0:
            if character.stat == "player":
                players_alive = True
            elif character.stat == "NPC":
                npcs_alive = True

    if players_alive and npcs_alive:
        return None

    elif players_alive:
        return "player"

    elif npcs_alive:
        return "NPC"

    else:
        return "draw"


def attack(source, target, attack_modifier, damage): # return True if hit, False if miss
    """Roll a D20 with an attack modifier and return whether it hits the target's armour class."""
    roll = random.randint(1, 20)
    total = roll + attack_modifier

    story_print(f"\n{source.character_class if isinstance(source, Player) else source.name} Attack Roll\n", 100, "character")
    story_print(f"D20:      {roll}", 100, "character")
    story_print(f"Modifier: {attack_modifier:+d}", 100, "character")
    story_print(f"Total:    {total}\n", 100, "character")

    if total >= target.armour:
        story_print("HIT!", 100, "word")
        target.current_hp = max(0, target.current_hp - damage)
        story_print(f"{target.character_class if isinstance(target, Player) else target.name} takes {damage} damage.", 100, "character")
        story_print(f"HP: {target.current_hp}/{target.maximum_hp}", 100, "word")
        if target.current_hp == 0:
            target_name = target.character_class if isinstance(target, Player) else target.name
            story_print(f"{target_name} faints!", 100, "character")            

        else:
            story_print("The target is still standing!", 100, "character")
        return True
    else:
        story_print("MISS!\n", 100, "word")
        story_print("the target is still standing!", 100, "character")
        return False

def combat():
    """Resolve one round of player and NPC attacks in initiative order."""
    # Initiative_tracker already sorts the highest initiative first.
    escaped = False
    for entry in Initiative_order:
        attacker = entry["character"]
        if attacker.current_hp <= 0:
            continue

        target = None
        if isinstance(attacker, Player):
            story_print("Your turn, please select action:", 100, "character")
            story_print("1. Fight\n2. Disengage\n", 100, "character")
            while True:
                choice = input("> ").strip()
                if choice == "1":
                    for target_entry in Initiative_order:
                        character = target_entry["character"]
                        if character.stat == "NPC" and character.current_hp > 0:
                            target = character
                            break
                    break
                elif choice == "2":
                    # Dexterity check DC 12. Success escapes combat; failure ends the player's turn.
                    if ability_check(attacker, attacker.dexterity, 12, "Disengage"):
                        story_print("You successfully disengage from combat and retreat to a safe distance.", 100, "character")
                        escaped = True
                    else:
                        story_print("You fail to disengage from combat.", 100, "character")
                    break

                else:
                    print("Please enter 1, or 2.")
            if escaped:
                return "escaped"

            if choice == "2":
                continue

            if target is None:
                return

            attack_modifier = (attacker.attack_ability - 10) // 2
            attack(attacker, target, attack_modifier, attacker.damage)
        elif attacker.stat == "NPC":
            for target_entry in Initiative_order:
                character = target_entry["character"]

                if isinstance(character, Player) and character.current_hp > 0:
                    target = character
                    break

            if target is None:
                return

            attack(attacker,target,attacker.attack_modifier,attacker.damage)
    return 


def ability_check(player, ability_score, dc, check_name):
    """Roll a D20 with an ability modifier and return whether it meets the DC."""

    roll = random.randint(1, 20)
    modifier = (ability_score - 10) // 2
    bonus = player.skill_check_bonus

    total = roll + modifier + bonus

    story_print(f"\n{check_name} Check — DC {dc}\n", 100, "word")
    story_print(f"D20:      {roll}", 100, "word")
    story_print(f"Modifier: {modifier:+d}", 100, "word")

    if bonus >0:
        story_print(f"Potion:   {bonus:+d}", 100, "word")

    story_print(f"Total:    {total}\n", 100, "word")
    # The potion bonus only applies to one ability check.
    player.skill_check_bonus = 0

    if total >= dc:
        story_print("SUCCESS", 100, "word")
        return True
    else:
        story_print("FAILURE", 100, "word")
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
    enter_room_two(player)
    story_pause()


if __name__ == "__main__":
    main()
