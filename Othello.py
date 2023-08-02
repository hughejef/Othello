# Author: Jeffrey Hughes
# GitHub username: HugheJef
# Date: 05/29/2023
# Description: A game of Othello


class Player:
    """
    Represents a player object that receives both a name and a color
    """
    def __init__(self, name, color):
        self._name = name
        self._color = color


    def get_name(self):
        """
        Returns name of player
        """
        return self._name

    def get_color(self):
        """
        Returns color of player
        """
        return self._color


class Othello:
    """
    Represents a game of Othello
    """

    def __init__(self):
        self._board = [
            ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],  # 0
            ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],  # 1
            ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],  # 2
            ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],  # 3
            ['*', '.', '.', '.', 'O', 'X', '.', '.', '.', '*'],  # 4
            ['*', '.', '.', '.', 'X', 'O', '.', '.', '.', '*'],  # 5
            ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],  # 6
            ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],  # 7
            ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],  # 8
            ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*']  # 9
        ]  # 0    1    2    3    4    5    6    7    8    9

        self._player_list = []
        self._moves_dict = {}
        self._winner = "It's a tie"

    def get_moves_dict(self):
        """
        Returns moves_dict which is populated by the return_available_positions methods. a dictionary entry is created
        with a concatenation of starting coord and ending coord as the key, and a list of all the coordinates as the
         values. This makes it easy to update all coordinates in the line with the player's color when appropriate
         """
        return self._moves_dict

    def clear_moves_dict(self):
        """
        Erases all data in moves_dict. Rather than adding and removing move lists from the dicitonary, the moves_dict
        will just be re-populated every time available positions are checked and then cleared before used again.
        """
        self._moves_dict = {}

    def print_board(self):
        """
        Prints the current board with up-to-date positioning visualized for all pieces played on the board
        up to this point. By default, O's and X's are placed in their default, diagonal starting positions. The board
        itself is a data member of the Othello class and the print_board method should print the layout of how the
        board (an array) appears at any given time. This will be called by the make_move method as players should see
        a visualization of how the board appears after a move is made.
        """
        for row in self._board:
            print(" ".join(row))

    def create_player(self, name, color):
        """
        Creates a new player within a game of Othello
        """
        self._player_list.append(Player(name, color))

    def return_winner(self):
        """
        Returns the winner of Othello game
        """
        return self._winner

    def get_player_list(self):
        """
        Returns list of players within an Othello game
        """
        return self._player_list

    def get_player_name(self, color):
        """
        Returns the name of a player for a given color passed as a parameter
        """
        for player_object in self._player_list:
            if player_object.get_color() == color:
                return player_object.get_name()

    def get_occupied_spaces(self, color):
        """
        Returns a list of coordinates that a given player (passed as parameters to the function) has a piece in.
        This list is used by the return_available_positions method as in order to determine which moves a player can
        make, we must first know where they player's pieces lay.
        """
        occupied_spaces = []

        # setting X and O variables for iterating through the board and linking to color
        if color == "black":
            color = "X"
        if color == "white":
            color = "O"

        for row in range(len(self._board)):
            for column in self._board[row]:
                if color == column:
                    column_pos = -1
                    while True:
                        try:
                            column_pos = self._board[row].index(column, column_pos + 1 )
                            if (row, self._board[row].index(column, column_pos)) not in occupied_spaces:
                                occupied_spaces.append((row, self._board[row].index(column, column_pos)))
                        except ValueError:
                            break
        return occupied_spaces

    def return_available_positions(self, color):
        """
        Returns a list of possible positions a player (passed as a parameter by their color) is able to place a piece
        based on current board positions.
        This will be a return of the current values making up the lists
        self._white_available_positions or
        self._black_available_positions
        where are Othello private data members.
        """
        # setting X and O variables for iterating through the board and linking to color
        if color == "black":
            color = "X"
        if color == "white":
            color = "O"

        available_positions = []

        def check_adj():
            """
            Internal function within the return_available_positions method that acts as a helper function by first
            checking all adjacent spaces to the specified player's pieces and then checking for valid moves. The first
            step for determining if a valid move might exist down a line is to check that an adjacent space has the
            opponent's piece in it. This function first checks for that and then, if yes, passes the coordinate to
            the recursive function rec_check_adj until finality.
            """
            for coordinate in self.get_occupied_spaces(color):
                if self._board[coordinate[0] - 1][coordinate[1] + 0] not in [color, '*', '.']:  # - row
                    temp_line = [coordinate]
                    next_coord = (coordinate[0] - 1, coordinate[1] + 0)
                    temp_line.append(next_coord)
                    row_change = next_coord[0] - coordinate[0]
                    col_change = next_coord[1] - coordinate[1]
                    rec_check_adj(coordinate, next_coord, row_change, col_change,temp_line)
                if self._board[coordinate[0] + 1][coordinate[1] + 0] not in [color, '*', '.']:  # + row
                    temp_line = [coordinate]
                    next_coord = (coordinate[0] + 1, coordinate[1] + 0)
                    temp_line.append(next_coord)
                    row_change = next_coord[0] - coordinate[0]
                    col_change = next_coord[1] - coordinate[1]
                    rec_check_adj(coordinate, next_coord, row_change, col_change,temp_line)
                if self._board[coordinate[0] + 0][coordinate[1] + 1] not in [color, '*', '.']:  # + column
                    temp_line = [coordinate]
                    next_coord = (coordinate[0] + 0, coordinate[1] + 1)
                    temp_line.append(next_coord)
                    row_change = next_coord[0] - coordinate[0]
                    col_change = next_coord[1] - coordinate[1]
                    rec_check_adj(coordinate, next_coord, row_change, col_change,temp_line)
                if self._board[coordinate[0] + 0][coordinate[1] - 1] not in [color, '*', '.']:  # - column
                    temp_line = [coordinate]
                    next_coord = (coordinate[0] + 0, coordinate[1] - 1)
                    temp_line.append(next_coord)
                    row_change = next_coord[0] - coordinate[0]
                    col_change = next_coord[1] - coordinate[1]
                    rec_check_adj(coordinate, next_coord, row_change, col_change,temp_line)
                if self._board[coordinate[0] + 1][coordinate[1] + 1] not in [color, '*', '.']:  # + row + column
                    temp_line = [coordinate]
                    next_coord = (coordinate[0] + 1, coordinate[1] + 1)
                    temp_line.append(next_coord)
                    row_change = next_coord[0] - coordinate[0]
                    col_change = next_coord[1] - coordinate[1]
                    rec_check_adj(coordinate, next_coord, row_change, col_change,temp_line)
                if self._board[coordinate[0] + 1][coordinate[1] - 1] not in [color, '*', '.']:  # + row - column
                    temp_line = [coordinate]
                    next_coord = (coordinate[0] + 1, coordinate[1] - 1)
                    temp_line.append(next_coord)
                    row_change = next_coord[0] - coordinate[0]
                    col_change = next_coord[1] - coordinate[1]
                    rec_check_adj(coordinate, next_coord, row_change, col_change,temp_line)
                if self._board[coordinate[0] - 1][coordinate[1] - 1] not in [color, '*', '.']:  # - row - column
                    temp_line = [coordinate]
                    next_coord = (coordinate[0] - 1, coordinate[1] - 1)
                    temp_line.append(next_coord)
                    row_change = next_coord[0] - coordinate[0]
                    col_change = next_coord[1] - coordinate[1]
                    rec_check_adj(coordinate, next_coord, row_change, col_change,temp_line)
                if self._board[coordinate[0] - 1][coordinate[1] + 1] not in [color, '*', '.']:  # - row + column
                    temp_line = [coordinate]
                    next_coord = (coordinate[0] - 1, coordinate[1] + 1)
                    temp_line.append(next_coord)
                    row_change = next_coord[0] - coordinate[0]
                    col_change = next_coord[1] - coordinate[1]
                    rec_check_adj(coordinate, next_coord, row_change, col_change,temp_line)


        def rec_check_adj(orig_coord, curr_coord, row_change, col_change,temp_line):
            """
            Recursive function to check if the next space in a row (that is confirmed to be confirmed to at least be
            player -> opponent -> ...) is followed by an empty space. An empty space in this function would mean that
            the player can make a valid move to that space. If the space contains the opponent's piece, then we need
            to move onto the next space. A * would indicate that we've reached the end and there is no valid move.
            """
            next_coord = ((curr_coord[0] + row_change), curr_coord[1] + col_change)
            if self._board[next_coord[0]][next_coord[1]] == '.':
                if next_coord not in available_positions:
                    available_positions.append(next_coord)
                temp_line.append(next_coord)
                # Need to do a try/except/else because one piece placement may affect more than one line
                try:
                    self._moves_dict[next_coord]
                except KeyError:
                    self._moves_dict[next_coord] = temp_line
                else:
                    # if the coordinate is already a possible move from another line, the list of coords should be
                    # appended rather than overridden
                    for space in temp_line:
                        self._moves_dict[next_coord].append(space)
            elif self._board[next_coord[0]][next_coord[1]] not in ['*',color]:
                temp_line.append(next_coord)
                rec_check_adj(orig_coord,next_coord, row_change, col_change, temp_line)

        check_adj()

        for pass_num in range(len(available_positions) - 1):
            for index in range(len(available_positions) - 1 - pass_num):
                if available_positions[index] > available_positions[index + 1]:
                    temp = available_positions[index]
                    available_positions[index] = available_positions[index + 1]
                    available_positions[index + 1] = temp

        return available_positions

    def check_game_over(self):
        """
        Checks for game over status by checking list of available moves for each player. If both players have
        no moves in their list, then the game is over. This is checked after every make_move method is executed
        """

        black_list = self.return_available_positions("black")
        white_list = self.return_available_positions("white")

        if len(black_list) == 0:
            if len(white_list) == 0:
                black_count = len(self.get_occupied_spaces("black"))
                white_count = len(self.get_occupied_spaces("white"))
                print(f"Game is ended white piece: {white_count} black piece: {black_count}")
                if black_count > white_count:
                    self._winner = "Winner is black player: " + self.get_player_name("black")
                if white_count > black_count:
                    self._winner = "Winner is white player: " + self.get_player_name("white")
                print(self.return_winner())

    def play_game(self, color, piece_position):
        """
        Takes, as a parameter, a player color and position, and tries to place a specified piece in the specified
        position. If the position passed is valid, then the move will be made (via the make_move method) and the board
        will be updated. If the position is invalid, the piece will not be placed and "Invalid Move" will be returned
        to the player along with a list of valid moves. If there are no valid moves, then an empty list is returned and
        the turn moves to the next player. If neither player has a valid move, then the game is over and
        the return_winner method should be called.
        """
        if color == "black":
            color = "X"
        if color == "white":
            color = "O"

        available_positions = self.return_available_positions(color)
        if piece_position in available_positions:
            self.make_move(color, piece_position)
            self.check_game_over()
            self.clear_moves_dict()
        else:
            print("Here are the valid moves:", str(available_positions))
            return "Invalid move"



    def make_move(self, color, piece_position):
        """
        Places a piece of the specified color at the position passed (piece_position) and updates the board.
        Once updated, the current visualization of the board should be returned via the print_board method.
        The make_move method is called by the play_game method and should not specifically be called by the user.
        make_move will also flip the colors of any opposing piece that are between the newly placed piece and the
        piece at the end of any applicable line.
        """
        if color == "black":
            color = "X"
        if color == "white":
            color = "O"
        try:
            for space in self._moves_dict[piece_position]:
                self._board[space[0]][space[1]] = color
        except KeyError:
            self.play_game(color, piece_position)
        self.print_board()
        return self._board

"""
game = Othello()
game.create_player("Helen", "white")
game.create_player("Leo", "black")
game.print_board()
game.return_available_positions("black")

game.play_game("black", (6,5))
game.play_game("white", (6,6))
game.play_game("black", (3,4))
game.play_game("white", (7,5))
game.play_game("black", (8,5))
game.play_game("white", (3,3))
game.play_game("black", (5,7))
game.play_game("white", (3,5))
game.play_game("black", (2,5))
game.play_game("white", (5,6))
game.play_game("black", (3,2))
game.play_game("white", (7,7))
game.play_game("black", (8,8))
game.play_game("white", (2,3))
game.play_game("black", (1,3))
game.play_game("white", (7,4))
game.play_game("black", (6,7))
game.play_game("white", (6,8))
game.play_game("black", (8,3))
game.play_game("white", (4,8))
game.play_game("black", (4,7))
game.play_game("white", (4,6))
game.play_game("black", (3,8))
game.play_game("white", (8,6))
game.play_game("black", (5,8))
game.play_game("white", (8,4))
game.play_game("black", (8,7))
game.play_game("white", (2,8))
game.play_game("black", (7,6))
game.play_game("white", (6,4))
game.play_game("black", (7,8))
game.play_game("white", (5,3))
game.play_game("black", (1,8))
game.play_game("white", (1,5))
game.play_game("black", (6,2))
game.play_game("white", (4,2))
game.play_game("black", (3,1))
game.play_game("white", (5,2))
game.play_game("black", (5,1))
game.play_game("white", (1,2))
game.play_game("black", (3,6))
game.play_game("white", (2,6))
game.play_game("black", (1,6))
game.play_game("white", (3,7))
game.play_game("black", (2,7))
game.play_game("white", (4,1))
game.play_game("black", (2,2))
game.play_game("white", (1,4))
game.play_game("black", (1,1))
game.play_game("white", (6,3))
game.play_game("black", (2,4))
game.play_game("white", (4,3))
game.play_game("black", (7,3))
game.play_game("white", (2,1))
game.play_game("black", (6,1))
game.play_game("white", (7,1))
game.play_game("black", (8,1))
game.play_game("white", (7,2))
game.play_game("black", (8,2))
"""