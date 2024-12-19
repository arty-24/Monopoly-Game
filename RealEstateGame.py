"""
# Arturo Osorio
# arty-24
# This program is a simulation of the board game Monopoly.
"""


class RealEstateGame:
    """A class to represent the monopoly game. Players start at the go space."""
    def __init__(self):
        """initializer for real estate game"""
        self._go_space = BoardSpace(0, "GO")
        self._players = []
        self._spaces = [self._go_space]

    def create_spaces(self, go_money, rent_list):
        """ Creates a space named GO along with 24 other spaces """
        self._go_space._rent_amount = go_money
        for index, rent in enumerate(rent_list):
           space_name = str(index+1)
           self._spaces.append(BoardSpace(rent, space_name))


    def create_player(self, name, account_balance):
        """Creates board game players"""
        new_player_object = Player(account_balance, name)
        self._players.append(new_player_object)

    def get_player_account_balance(self, name):
        """Returns the account balance of an existing player"""
        for player in self._players:
            if player.get_name() == name:
                return player.get_account_balance()
        return None

    def get_player_current_position(self, name):
        """" Returns the current position of the player """
        for player in self._players:
            if player.get_name() == name:
                return player.get_position()
        return None

    def buy_space(self, name):
        """ Allows a player to buy the current space if it is unowned and affordable """
        for player in self._players:
            if player.get_name() == name:
                current_position =  player.get_position()
                space = self._spaces[current_position]
                if space.get_owner() is None and player.get_account_balance() >= space.get_purchase_price():
                    player.decrease_account_balance(space.get_purchase_price())
                    space.set_owner(player.get_name())
                    return True
                return False
        return False

    def move_player(self, name, dice_roll):
        """Moves a player based on dice roll, processes GO rewards, and handles rent """
        for player in self._players:
            if player.get_name() == name:
                if player.get_account_balance() <= 0:
                    return None # player is inactive

                # update position
                new_position = (player.get_position() + dice_roll) % len(self._spaces)
                player.position = new_position

                # check GO space
                if new_position == 0:
                    player.increase_account_balance(self._go_space.get_rent_amount())

                # handle rent payment if space is owned
                space = self._spaces[new_position]
                if space.get_owner() is not None and space.get_owner() != player.get_name():
                    rent_amount = space.get_rent_amount()
                    if player.get_account_balance() >= rent_amount:
                        player.decrease_account_balance(rent_amount)
                        for owner in self._players:
                            if owner.get_name() == space.get_owner():
                                owner.increase_account_balance(rent_amount)
                    else:
                        player.decrease_account_balance(player.get_account_balance()) # bankrupt player

                return True
        return False


    def check_game_is_over(self):
        """ Checks if game is over. Either returns winners name or an empty space """
        active_players = [player for player in self._players if player.get_account_balance() > 0]
        if len(active_players) == 1:
            return active_players[0].get_name()
        return ""


class Player:
    """
    A class that initializes creation of board player
    The player will have a name, an account balance, and a start position at GO.
    """
    def __init__(self, account_balance, name):
        self._account_balance = account_balance
        self._name = name
        self._position = 0 # starting position

    def get_name(self):
        """ Returns the player's name """
        return self._name

    def get_account_balance(self):
        """ Returns the player's account balance """
        return self._account_balance

    def increase_account_balance(self, amount):
        """ Increases the player's account balance """
        self._account_balance += amount

    def decrease_account_balance(self, amount):
        """ Decreases the player's account balance """
        self._account_balance -= amount

    def get_position(self):
        """Returns the player's current position"""
        return self._position


class BoardSpace:
    """Represents a space on the game board"""
    def __init__(self, rent_amount, name):
        self._rent_amount = rent_amount
        self._purchase_price = rent_amount * 5
        self._owner = None  # All spaces are unowned at the beginning
        self._space_name = name

    def get_rent_amount(self):
        """Returns the rent amount for the space"""
        return self._rent_amount

    def get_purchase_price(self):
        """Returns the purchase price of the space"""
        return self._purchase_price

    def get_owner(self):
        """Returns the owner of the space"""
        return self._owner

    def set_owner(self, owner):
        """Sets the owner of the space"""
        self._owner = owner

game = RealEstateGame()

rent_list = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280]
go_money = 200
game.create_spaces(go_money, rent_list)

game.create_player("Arturo", 1500)
game.create_player("Remy", 1500)

print("Arturo's Balance:", game.get_player_account_balance("Arturo"))
print("Remys's Balance:", game.get_player_account_balance("Remy"))

game.move_player("Arturo", 5)
print("Arturo's Position:", game.get_player_current_position("Arturo"))

game.buy_space(5)
print("Owner of Space 5:", game._spaces[5].get_owner())

game.move_player("Bob", 5)
print("Remy's Balance after rent:", game.get_player_account_balance("Remy"))

print("Game Over:", game.check_game_is_over())

game.move_player("Bob", 20)
print("Remy's Balance after bankrupt move:", game.get_player_account_balance("Remy"))
print("Game Over:", game.check_game_is_over())





