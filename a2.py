# DO NOT modify or add any import statements
from a2_support import *
import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Optional, Callable

# Write your classes and functions here
def play_game(root: tk.Tk, file_path: str) -> None:
    """
    Description: Initializes, starts the game by setting up the game's controller and main loop.

    Parameters:
        root (tk.Tk): root window of the Tkinter module.
        file_path (str): file path to the level file

    Return:
        None
    """
    root.title("Into The Breach")
    root.mainloop()

def main() -> None:
    """
    Description: Sets up the tkinter window and starts the intothebreach game.

    Parameters:
        None

    Return:
        None
    """
    root = tk.Tk()
    play_game(root, 'levels/level1.txt')

if __name__ == "__main__":
    main()

#4.1 model
class Tile:
    """ Tile is an abstract class from which all instantiated types of tile inherit. Provides default tile be
    havior, which can be inherited or overridden by specific types of tiles."""

    def __repr__(self) -> str:
        """
        Description: Returns string, constructs identical instnce of tile"

        Parameters:
            None

        Return:
            str: returns string representation of tile instance
        """
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        """
        Description: Returns the character that is representing the tile type.

        Parameters:
            None

        Return:
            str: character that represents the tile
        """
        return TILE_SYMBOL



    def get_tile_name(self) -> str:
        """
        Description: Returns name of type of tile (i.e. name of the class of the tile)

        Parameters:
            None

        Return:
            str: name of tile type.
        """
        return self.__class__.__name__

    def is_blocking(self) -> bool:
        """
        Description: Returns whether the tile blocking, returns True only if the tile is blocking

        Parameters:
            None

        Return:
            bool: Default behaviour: False, meaning tiles not blocking
        """
        return False


class Ground(Tile):
    """ Ground inherits from Tile. Ground tiles represent simple, walkable ground with no special proper
    ties. Ground tiles are never blocking and are represented by a space character (’ ’)."""

    def __str__(self) -> str:
        """
        Description: Returns ground tile character representation: (' ')

        Parameters:
            None

        Return:
            str: character representation of ground tile.
        """
        return GROUND_SYMBOL

    def get_tile_name(self) -> str:
        """
        Description: Returns name of ground tile: ('Ground').

        Parameters:
            None

        Return:
            str: tile name 'Ground'.
        """
        return GROUND_NAME

    def is_blocking(self) -> bool:
        """
        Description: Returns the ground tile's blocking property'

        Parameters:
            None

        Return:
            bool: Always False-ground tiles never blocking.
        """
        return False

class Mountain(Tile):
    """Mountain inherits from Tile. Mountain tiles represent unpassable terrain. Mountain tiles are always
    blocking and are represented by the character M."""

    def __str__(self) -> str:
        """
        Description: Returns  mountain tile character ('M').

        Parameters:
            None

        Return:
            str: character that is representing a mountain tile ('M').
        """
        return MOUNTAIN_SYMBOL

    def get_tile_name(self) -> str:
        """
        Description: Returns name of mountain tile("Mountain").

        Parameters:
            None

        Return:
            str: name of tile- 'Mountain'.
        """
        return MOUNTAIN_NAME

    def is_blocking(self) -> bool:
        """
        Description: Return mountain tile blocking property

        Parameters:
            None

        Return:
            bool: Always True, because mountain tiles are always blocking.
        """
        return True
class Building(Tile):
    """ Building inherits from Tile. Building tiles represent one or more buildings that the player must
    protect from enemies. Building tiles have an integer health value and can be destroyed. """

    def __init__(self, initial_health: int) -> None:
        """
        Description: Will initialise building health set between 0-9, inclusive .

        Parameters:
            intitial_health(int): Health of the building.

        Return:
            None
        """
        if 0 <= initial_health <= 9: # initial health cannot be negative or above 9
            self.health = initial_health
        else:
            raise ValueError("Health of building tile must be between 0- 9, inclusive")
    def get_tile_name(self) -> str:
        """
        Description: Returns  name of building tile ("Building").

        Parameters:
            None

        Return:
            string: the name "Building".
        """
        return BUILDING_NAME

    def is_destroyed(self) -> bool:
        """
        Description: Function checks if the building is destroyed

        Parameters:
            None

        Return:
            bool: True if building is destroyed (health under or equal to 0)
                False otherwise.
        """
        return self.health <= 0

    def damage(self, damage: int) -> None:
        """
        Description: Reduces health of the building by the amount specified.

        Parameters:
            damage(int): amount of damage given.

        Return:
            None
        """
        if self.is_destroyed() == False:
            self.health -= damage
            # Health is capped between 0 & 9 health
            self.health = max(0, min(self.health, 9))

    def __repr__(self) -> str:
        """
        Description: Returns representation of the building: building name and health.

        Parameters:
            None

        Return:
            str: tile name and health if building not destroyed or
                 tile name if building destroyed
        """
        if self.is_destroyed() == False:
            return f"{self.get_tile_name()}({self.health})"
        else:
            return f"{self.get_tile_name()}()"

    def __str__(self) -> str:
        """
        Description: Returns string representation of the building's remaining health

        Parameters:
            None

        Return:
            str: remaining health of the building as a string.
        """
        return str(self.health)

    def is_blocking(self) -> bool:
        """
        Description: Returns if build tile is blocking
        Parameters:
            None

        Return:
            bool: True if the building tile is not destroyed (blocking)
                , False otherwise.
        """
        if self.is_destroyed() == False:
            return True
        else:
            return False

class Board:
    """ Board represents a structured set of tiles. A board organizes tiles in a rectangular grid, where each
 tile has an associated (row, column) position. (0,0) represents the top-left corner, (1,0) represents
 the position directly below the top-left corner, and (0, 1) represents the position directly right of the
 top left corner."""

    def __init__(self, board: list[list[str]]) -> None:
        """
        Description: Initialises game board with layout.

        Parameters:
            board (list[list[str]]): board layout

        Return:
            None
        """
        self.board = board

    def __repr__(self) -> str:
        """
        Description: Returns string representation of thee board object.

        Parameters:
            None

        Return:
            str: Board object's string representation
        """
        return f"Board({self.board})"

    def __str__(self) -> str:
        """
        Description: Returns the string representation of the board.

        Parameters:
            None

        Return:
            str  : the string representation of the board.
        """
        strings_rows= [''.join(row) for row in self.board]
        strings_board= '\n'.join(strings_rows)
        return strings_board

    def get_dimensions(self) -> tuple[int, int]:
        """
        Description: Returns the dimensions of the board

        Parameters:
            None

        Return:
            tuple[int, int]: retrns dimensions of the board.
        """
        num_rows = len(self.board)
        if num_rows > 0:
            num_cols = len(self.board[0])
        else:
            num_cols = 0
        return (num_rows, num_cols)

    def get_tile(self, position: tuple[int, int]) -> Building:
        """
        Description: Returns building object at given specified.

        Parameters:
            position: (tuple[int, int]): position which to get the tile from

        Return:
            Building: building object at specfied position.
        """
        row, col = position
        tile_symbol = self.board[row][col]
        if tile_symbol.isdigit():
            return Building(int(tile_symbol))
        elif tile_symbol == MOUNTAIN_SYMBOL:
            return Building(0)
        else:
            return Building(0)

    def get_buildings(self) -> dict[tuple[int, int], Building]:
        """
        Description: functios that returns dictionary mapping positions of building objects

        Parameters:
            None

        Return:
            dict[tuple[int, int], Building]: returns a dictionary mapping positions to the building objects.
        """
        buildings = {}
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j].isdigit(): # if all characters are numbers
                    position = (i, j)
                    buildings[position] = Building(int(self.board[i][j]))
        return buildings


class Entity:
    """ Entity is an abstract class from which all instantiated types of entity inherit. This class provides
 default entity behavior, which can be inherited or overridden by specific types of entities."""

    def __init__(self, position, initial_health, speed, strength):
        """
        Description: Initialises a Entity with several attributes.

        Parameters:
            position(tuple[int, int]): inital psotition of the entity
            initial_health(int): entities initial health
            speed(int): speed of the entity.
            strength(int): strength of entity.

        Return:
            None
        """
        self._position =position
        self._health = initial_health
        self._speed= speed
        self._strength =strength

    def __repr__(self):
        """
        Description: Returns string representation of entity object.

        Parameters:
            None

        Return:
            string: entity objects string representation
        """
        return (f"{self.__class__.__name__}({self._position},"
                f" {self._health},"
                f" {self._speed},"
                f" {self._strength})") #all entity attributes

    def __str__(self):
        """
        Description: Returns entity's attributes

        Parameters:
            None

        Return:
            string: string representation of the specific entity's attributes.
        """
        return (f"{self.get_symbol()},"
                f"{self._position[0]},"
                f"{self._position[1]},"
                f"{self._health},"
                f"{self._speed},"
                f"{self._strength}")

    def get_symbol(self):
        """
        Description: Returns character that represents the entity.

        Parameters:
            None

        Return:
            str: character which represents the entity.
        """
        return ENTITY_SYMBOL

    def get_name(self):
        """
         Description: Returns entity name

         Parameters:
             None

         Return:
             str: Entity name
         """
        return ENTITY_NAME

    def get_position(self):
        """
        Description: Returns current position of entity.

        Parameters:
            None

        Return:
            tuple[int, int]: current position of entity.
        """
        return self._position

    def set_position(self, position):
        """
        Description: Sets the position of the entity.

        Parameters:
            position (tuple[int, int]): The new position of the entity.

        Return:
            None
        """
        self._position = position

    def get_health(self):
        """
        Description: Returns current health of entity..

        Parameters:
            None

        Return:
            int: current health of the entity.
        """
        return self._health

    def get_speed(self):
        """
        Description: returns entity's speed

        Parameters:
            None

        Return:
            int: speed of the entity.
        """
        return self._speed

    def get_strength(self):
        """
        Description: Returns entity's speed

        Parameters:
            None

        Return:
            int: strength of entiity
        """
        return self._strength

    def damage(self, damage):
        """
        Description: Inflicts damage (reduce health) to specific entity

        Parameters:
            damage  (int): amount of damage inflicted.

        Return:
            None
        """
        if self.is_alive() == False:
            return

        self._health -= damage
        # ensure health cant go lower than zero
        self._health = max(0, self._health)

    def is_alive(self):
        """
        Description: Returns based on whether entity is alive or not.

        Parameters:
            None

        Return:
            bool: True if the entity alive (health above zero), False otherwise.
        """
        if self._health >0:
            return True
        else:
            return False

    def is_friendly(self):
        """
        Description: Returns False ( the entity is not friendly)

        Parameters:
            None

        Return:
            bool: False (entity is not friendly)
        """
        return False

    def get_targets(self):
        """
        Description: Returns default target positions (adjacent tiles: up, down, left, and right).

        Parameters:
            None

        Return:
            list[tuple[int, int]]: list of target positions.
        """
        row, col = self._position
        return [(row, col + 1), #up
                (row, col - 1), # down direction
                (row + 1, col), #left
                (row - 1, col)] #right

    def attack(self, entity):
        """
        Description: Attacks another entity, inflicts damage relative to strength.

        Parameters:
            entity (Entity): specific entity to attack.

        Return:
            None
        """
        if self.is_alive() == False or entity.is_alive() ==False:
            return
        entity.damage(self._strength)

class Mech(Entity):
    """Mech is an abstract class that inherits from Entity from which all instantiated types of mech inherit.
    This class provides default mech behavior, which can be inherited or overridden by specific types of mechs."""

    def __init__(self, position, initial_health, speed, strength):
        """
        Description: Initializes a Mech entity with the different attributes

        Parameters:
            position (tuple[int, int]): inital position of Mech entity.
            initial_health (int): initial health of Mech.
            speed (int): speed of mech entity.
            strength (int): strength of mech.

        Return:
            None
        """
        super().__init__(position, initial_health, speed, strength)
        self._active = True
        self._previous_position = None

    def enable(self):
        """
        Description: Enables mech entity, makes it active

        Parameters:
            None

        Return:
            None
        """
        self._active = True

    def disable(self):
        """
        Description: Disables the mech entity, makes it inactive.

        Parameters:
            None

        Return:
            None
        """
        self._active= False

    def is_active(self):
        """
        Description: Returns True if Mech is active, else returns False.

        Parameters:
            None

        Return:
            bool: True if Mech is active,  False otherwise.
        """
        return self._active

    def get_symbol(self):
        """
        Description: Returns character represenation of the Mech.

        Parameters:
            None

        Return:
            str: character representing mech entiity.
        """
        return MECH_SYMBOL

    def get_name(self):
        """
        Description: Returns name of the Mech.

        Parameters:
            None

        Return:
            str: name of the mech.
        """
        return MECH_NAME

    def is_friendly(self):
        """
        Description: Returns True (as Mech is friendly)

        Parameters:
            None

        Return:
            bool: True (mech is friendly)
        """
        return True

    def set_position(self, position):
        """
        Description: sets position of the Mech (updates from its previous position)

        Parameters:
            position (tuple[int, int]): mech's new position

        Return:
            None
        """
        self._previous_position = self.get_position()
        super().set_position(position)

    def get_previous_position(self):
        """
        Description: Returns previous position of the Mech entity

        Parameters:
            None

        Return:
            tuple[int, int]: previous pos of Mech entity.
        """
        return self._previous_position

class TankMech(Mech):
    """ TankMech inherits from Mech. TankMech represents a type of mech that attacks at a long range
    horizontally. """

    def __init__(self, position, initial_health, speed, strength):
        """
        Description: initialises a TankMech with various attributes.

        Parameters:
            position (tuple[int, int]): initial pos of the TankMech.
            initial_health (int): tankmech's initial health.
            speed (int): The speed of the TankMech.
            strength (int): The strength of the Tankmech.

        Return:
            None
        """
        super().__init__(position, initial_health, speed, strength)

    def get_symbol(self):
        """
        Description: Returns the character representing the TankMech.

        Parameters:
            None

        Return:
            str: character that represents the TankMech.
        """
        return TANK_SYMBOL

    def get_name(self):
        """
        Description: Returns name of the TankMech.

        Parameters:
            None

        Return:
            str: Name of the TankMech.
        """
        return TANK_NAME

    def get_targets(self):
        """
        Description: Returns the target positions for TankMech (longer range, horizontal direction).

        Parameters:
            None

        Return:
            list[tuple[int, int]]: list of target positions.
        """
        row, col = self.get_position()
        targets = []
        # will attack longer range, in horizontal direction
        for attack_range in range(1, 6):  # range of 5 tiles (each direction) to attack
            targets.append((row, col + attack_range))  # Right direction
            targets.append((row, col - attack_range))  # Left
        return targets

class HealMech(Mech):
    """ HealMech inherits from Mech. HealMech represents a type of mech that does not deal damage, but
    instead supports friendly units and buildings by healing """

    def __init__(self, position, initial_health, speed, strength):
        """
        Description: initialises a HealMech with various given attributes.

        Parameters:
            position (tuple[int, int]): initial position of the HealMech.
            initial_health (int): initial health of the HealMech.
            speed (int): speed of the HealMech.
            strength (int): strength of the HealMech.

        Return:
            None
        """
        super().__init__(position, initial_health, speed, strength)

    def get_symbol(self):
        """
        Description: Returns the symbol representing the HealMech.

        Parameters:
            None

        Return:
            str: The symbol represnting the HealMech.
        """
        return HEAL_SYMBOL

    def get_name(self):
        """
        Description: Returns name of the HealMech.

        Parameters:
            None

        Return:
            str: Name of the HealMech.
        """
        return HEAL_NAME

    def get_strength(self):
        """
        Description: Returns strength of the HealMech as negative value (negative damage=healing).

        Parameters:
            None

        Return:
            int: negative of the strength of the HealMech.
        """
        return -self._strength  # neg strength for healing

    def attack(self, entity):
        """
        Description: inflicts friendly entity with negative damage (thus healing)

        Parameters:
            entity (Entity): entity to be healed

        Return:
            None
        """
        if self.is_alive()==False or entity.is_alive()== False or entity.is_friendly()== False:
            return
        entity.damage(-self._strength)  # friendly entities healed by neg damage

class Enemy(Entity):
    """ Enemy is an abstract class that inherits from Entity from which all instantiated types of enemy
    inherit. """

    def __init__(self, position, initial_health, speed, strength):
        """
        Description: intialises an Enemy with various given attributes.

        Parameters:
            position (tuple[int, int]): initial position of the Enemy.
            initial_health (int): initial health of the Enemy entity.
            speed (int): speed of the Enemy entity.
            strength (int): strength of the Enemy.

        Return:
            None
        """
        super().__init__(position, initial_health, speed, strength)
        self._objective = position  # objective initialised (to current position)

    def get_symbol(self):
        """
        Description: Returns the symbol representing Enemy.

        Parameters:
            None

        Return:
            str: The symbol representing the Enemy entity.
        """
        return ENEMY_SYMBOL

    def get_name(self):
        """
        Description: Returns name of the Enemy.

        Parameters:
            None

        Return:
            str: name of the enemy entity
        """
        return ENEMY_NAME

    def get_objective(self):
        """
        Description: Returns currnet objective of the Enemy.

        Parameters:
            None

        Return:
            tuple[int, int]: current objective of the Enemy entity.
        """
        return self.get_position()

    def update_objective(self, entities, buildings):
        """
        Description: Updates objective of enemy based on buildings and entities.
        Parameters:
            entities (list[Entity]): list of entities.
            buildings(dict[tuple[int, int], Building]): dictionary of buildings.

        Return:
            None
        """
        max_health = -1
        optimal_position = self.get_position()

        for entity in entities:
            if isinstance(entity, Mech)== True and entity.is_alive()== True:
                if entity.get_health() > max_health:
                    max_health = entity.get_health()
                    optimal_position = entity.get_position()

        self._objective = optimal_position

class Scorpion(Enemy):
    """ Scorpion inherits from Enemy. Scorpion represents a type of enemy that attacks at a moderate
    range in all directions, and targets mechs with the highest health. """

    def __init__(self, position, initial_health, speed, strength):
        """
        Description: Initializes Scorpion enemy with several given attributes.

        Parameters:
            position (tuple[int, int]): initial position of the Scorpion.
            initial_health (int): initial health of the Scorpion.
            speed (int): speed of the Scorpion.
            strength (int): The strength of the Scorpion enemy.

        Return:
            None
        """
        super().__init__(position, initial_health, speed, strength)

    def get_symbol(self):
        """
        Description: Returns the symbol representing the Scorpion.

        Parameters:
            None

        Return:
            str: The symbol that represents the Scorpion.
        """
        return SCORPION_SYMBOL

    def get_name(self):
        """
        Description: Returns name of the Scorpion.

        Parameters:
            None

        Return:
            str: name of the Scorpion.
        """
        return SCORPION_NAME

    def get_targets(self):
        """
        Description: Returns target positions for the scorpion enemy (medium-range, all directions).

        Parameters:
            None

        Return:
            list[tuple[int, int]]: list of target positions.
        """
        row, col = self.get_position()
        targets = []
        # scorpion attacks medium range, all directions
        for attack_range in range(1, 3):  # attack range: 2 tiles all directions
            targets.append((row, col + attack_range))  #Right direction
            targets.append((row, col - attack_range))  #left
            targets.append((row + attack_range, col))  #Down
            targets.append((row - attack_range, col))  #Up
        return targets

    def update_objective(self, entities, buildings):
        """
        Description: Updates the objective of the Scorpion based on nearby entities and buildings.

        Parameters:
            entities (list[Entity]): list of entities.
            buildings (dict[tuple[int, int], Building]): the dictionary of buildings.

        Return:
            None
        """
        max_health = -1
        optimal_position = self.get_position()
        for entity in entities:
            if isinstance(entity, Mech) and entity.is_alive()== True:
                entity_health= entity.get_health()
                if entity_health > max_health:
                    #checks if entity within the range
                    entity_position = entity.get_position()
                    if entity_position in self.get_targets():
                        max_health = entity_health
                        optimal_position =entity_position

        self._objective = optimal_position

    def get_objective(self):
        """
        Description: Returns Scorpion's current objective

        Parameters:
            None

        Return:
            tuple[int, int]: returns the current objective of the Scorpion.
        """
        return self._objective

class Firefly(Enemy):
    """ Firefly inherits from Entity. Firefly represents a type of enemy that attacks at a long range
    vertically, and targets buildings with the lowest health."""

    def __init__(self, position, health, speed, strength):
        """
        Description: intialises a Firefly enemy with several given attributes.

        Parameters:
            position (tuple[int, int]): the initial position of the Firefly enemy.
            initial_health (int): The initial health of the Firefly.
            speed (int): speed of the Firefly.
            strength (int): strength of the Firefly.

        Return:
            None
        """
        super().__init__(position, health, speed, strength)

    def get_symbol(self):
        """
        Description: Returns the symbol that represents the Firefly.

        Parameters:
            None

        Return:
            str: the symbol that represents the Firefly.
        """
        return FIREFLY_SYMBOL

    def get_name(self):
        """
        Description: Returns the name of the Firefly enemy.

        Parameters:
            None

        Return:
            str: name of the Firefly.
        """
        return FIREFLY_NAME

    def get_targets(self):
        """
        Description: Returns the available target positions for the Firefly.

        Parameters:
            None

        Return:
            list[tuple[int, int]]: the list of target positions.
        """
        targets = []
        for i in range(1, 6):
            targets.append((i, 0))
            targets.append((-i, 0))
        return targets

    def update_objective(self, entities, buildings):
        """
        Description: updates the objective of the Firefly based on the buildings, entities.

        Parameters:
            entities (list[Entity]): list of entities.
            buildings (dict[tuple[int, int], Building]): dictionary of buildings.

        Return:
            None
        """
        target_building =None
        min_health = float('inf')

        for pos, building in buildings.items():
            if pos in buildings and buildings[pos].health < min_health:
                min_health = buildings[pos].health
                target_building =pos

        self._objective = target_building

    def get_objective(self):
        """
        Description: returns the current objective of the Firefly enemy.

        Parameters:
            None

        Return:
            tuple[int, int]: the current objective of the Firefly enemy.
        """
        return self._objective

class BreachModel:
    """ BreachModel models the logical state of a game of IntoTheBreach"""

    def __init__(self,board: Board,entities: list[Entity])-> None:
        """
        Description: initalises the BreachModel with the previous board and entities.

        Parameters:
            board (Board): game board.
            entities (list[Entity]): list of entities.

        Return:
            None
        """
        self.board = board
        self.entities = entities

    def __str__(self) -> str:
        """
        Description: Returns string representation of BreachModel, including the board and the entities.

        Parameters:
            None

        Return:
            str: string representation of the BreachModel.
        """
        entity_strings = [str(entity) for entity in self.entities]
        return str(self.board) + '\n' + '\n'.join(entity_strings)

    def get_board(self) -> Board:
        """
        Description: returns the game board.

        Parameters:
            None

        Return:
            Board: game board.
        """
        return self.board

    def get_entities(self) -> list[Entity]:
        """
        Description: returns list of entities.

        Parameters:
            None

        Return:
            list[Entity]: list of entities.
        """
        return self.entities

    def has_won(self) -> bool:
        """
        Description: Returns True if the player won the game, else False.

        Parameters:
            None

        Return:
            bool: True if the player won the game, else False.
        """
        return True

    def has_lost(self) -> bool:
        """
        Description: Returns True if the player lost the game, else False.

        Parameters:
            None

        Return:
            bool: True if the player has lost, else false.
        """
        return True

    def entity_positions(self) -> dict[tuple[int, int], Entity]:
        """
        Description: Returns dictionary of entity positions mapped to the entities.

        Parameters:
            None

        Return:
            dict[tuple[int, int], Entity]: dictionary of entity positions mapped to entities.
        """
        return {entity.get_position(): entity for entity in self.entities}

    def get_valid_movement_positions(self, entity: Entity) -> list[tuple[int, int]]:
        """
        Description: Returns the list of valid movement positions for the specific entity.

        Parameters:
            entity (Entity): the specific entity for which to get valid movement positions for

        Return:
            list[tuple[int, int]]: list of valid movement positions for the entity.
        """
        current_position = entity.get_position()
        valid_positions = []

        for i in range(self.board.get_dimensions()[0]):
            for j in range(self.board.get_dimensions()[1]):
                if get_distance(current_position, (i, j)) <= entity.get_speed():
                    valid_positions.append((i, j)) # add to list of valid positions

        valid_positions.sort(key=lambda pos: (-pos[0], pos[1]))
        return valid_positions

    def attempt_move(self, entity: Entity, position: tuple[int, int]) -> None:
        """
        Description: Attempts to move the specific entity to the specifc position.

        Parameters:
            entity (Entity): the entity to move.
            position (tuple[int, int]): the position which the entity is to be moved to.

        Return:
            None
        """
        if entity.is_friendly() ==True and entity.is_active()== True and position in self.get_valid_movement_positions(entity):
            entity.set_position(position)
            entity.disable()

    def ready_to_save(self) -> bool:
        """
        Description: Returns true if game state is ready to be saved, else false.

        Parameters:
            None

        Return:
            bool: True if game state is ready to be saved, else False.
        """
        return True

    def end_turn(self)-> None:
        """
        Description: Ends the current turn, moves enemies, enables the friendly Mechs.

        Parameters:
            None

        Return:
            None
        """
        self.move_enemies()
        for entity in self.entities:
            if isinstance(entity, Mech):
                entity.enable()
