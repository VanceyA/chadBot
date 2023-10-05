import random

class Minesweeper:

    def __init__(self, size, num_mines):
        self._width = size
        self._height = size
        self._num_mines = num_mines
        self._board = [0 for _ in range(size*size)]
        self._mines = []
        self._emojis = {
            0: "||0️⃣||",
            1: "||1️⃣||",
            2: "||2️⃣||",
            3: "||3️⃣||",
            4: "||4️⃣||",
            5: "||5️⃣||",
            6: "||6️⃣||",
            7: "||7️⃣||",
            8: "||8️⃣||",
            9: "||9️⃣||",
            "mine": "||💣||"
        }

    def initialize_board(self):
        """Create the mines and numbers on the board."""
        self.create_mines()
        self.create_numbers()

    def create_mines(self):
        """Randomly place mines on the board."""
        index = random.randrange(len(self._board))
        for _ in range(self._num_mines):
            while index in self._mines:
                index = random.randrange(len(self._board))
            self._mines.append(index)

    def create_numbers(self):
        """Calculate and populate the numbers on the board."""
        for i in range(len(self._board)):
            if i not in self._mines:
                count = self.calculate_adjacent_mines(i)
                self._board[i] = self._emojis[count]
            else:
                self._board[i] = self._emojis["mine"]      

    def calculate_adjacent_mines(self, index):
        """Count the number of adjacent mines for a given cell."""
        count = 0
        
        if index % self._width != 0 and (index - 1) in self._mines:
            count += 1
        
        # LEFT SIDE
        if index % self._width != self._width - 1 and (index + 1) in self._mines:
            count += 1

        # BOTTOM SIDE
        if index >= self._width and (index - self._width) in self._mines:
            count += 1

        # TOP SIDE
        if index < self._width * (self._height - 1) and (index + self._width) in self._mines:
            count += 1

        # BOTTOM RIGHT
        if (index % self._width != 0 and index >= self._width and (index - self._width - 1) in self._mines):
            count += 1

        # BOTTOM LEFT
        if (index % self._width != self._width - 1 and index >= self._width and (index - self._width + 1)in self._mines):
            count += 1
        
        # TOP RIGHT
        if (index % self._width != 0 and index < self._width * (self._height - 1) and (index + self._width - 1) in self._mines):
            count += 1

        # TOP LEFT
        if (index % self._width != self._width - 1 and index < self._width * (self._height - 1) and (index + self._width + 1) in self._mines):
            count += 1    

        return count

    def get_board(self):
        """Get the current state of the game board as a string."""
        board_string = ""
        for i in range(self._height):
            start_index = i * self._width
            end_index = start_index + self._width
            row = self._board[start_index:end_index]
            board_string += " ".join(map(str, row)) + "\n"
        return board_string
    