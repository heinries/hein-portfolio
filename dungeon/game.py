"""The beginning of the Training Dungeon terminal adventure."""
import random


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
        elif character_class == "Rogue":
            self.strength = 10
            self.dexterity = 15
            self.constitution = 10
            self.intelligence = 12
            self.wisdom = 12
            self.charisma = 10
            self.maximum_hp = 10
            self.armour = 12
        elif character_class == "Wizard":
            self.strength = 8
            self.dexterity = 10
            self.constitution = 10
            self.intelligence = 15
            self.wisdom = 13
            self.charisma = 10
            self.maximum_hp = 8
            self.armour = 10
        else:
            raise ValueError("Choose Fighter, Rogue, or Wizard.")

        self.current_hp = self.maximum_hp
        self.steps = 0


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


def show_status(player):
    """Print the player's current status on one line."""
    print(
        f"Class: {player.character_class} | "
        f"HP: {player.current_hp}/{player.maximum_hp} | "
        f"Armour: {player.armour} | "
        f"Steps: {player.steps}"
    )


def show_character_sheet(player):
    """Print all six abilities and the player's health and armour when needed."""
    print(f"\n{player.character_class.upper()}")
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


def corridor_trap(player):
    """Resolve the corridor dart trap."""
    print("\nYou feel a stone beneath your boot sink into the floor. \nA dart shoots from the wall!")
    if ability_check(player.dexterity, 12, "Dexterity"):
        print("You dodge the dart!")
    else:
        print("The dart hits you! You take 2 damage.")
        player.current_hp -= 2


def enter_room_one(player):
    """Show the first room and carry out one chosen action."""
    print("\nRoom 1")
    print("The player opens an old door and dusty air fills the corridor.")
    print("The corridor is long and dark.\n")
    print("1. Walk forward")
    print("2. Light a torch")
    print("3. Stop and listen")

    while True:
        choice = input("> ").strip()

        if choice == "1":
            action = "Walk forward"
            roll = random.randint(1, 3)
            if roll == 1:
                print("CLICK!")
                print("You hear something move inside the wall...")
                corridor_trap(player)
            else:
                print("You carefully continue down the corridor.")
                      
        elif choice == "2":
            action = "Light a torch"
        elif choice == "3":
            action = "Stop and listen"
        else:
            print("Please enter 1, 2, or 3.")
            continue

        player.steps += 1
        print(f"\nYou selected: {action}.")
        show_status(player)
        return


def main():
    """Start the adventure and play the beginning of Room 1."""
    print("Welcome to the Adventurer's Guild!")
    print("Your training begins here.\n")

    player = choose_class()
    print()
    show_character_sheet(player)
    enter_room_one(player)


if __name__ == "__main__":
    main()
