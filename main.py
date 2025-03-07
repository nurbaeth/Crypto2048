import tkinter as tk
import random

GRID_SIZE = 4
CELL_SIZE = 100
GAP = 10
BACKGROUND_COLOR = "#bbada0"
EMPTY_CELL_COLOR = "#cdc1b4"
TILE_COLORS = {
    2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563", 32: "#f67c5f",
    64: "#f65e3b", 128: "#edcf72", 256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
}
FONT = ("Arial", 24, "bold")

class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 Game")
        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.init_ui()
        self.spawn_tile()
        self.spawn_tile()
        self.update_ui()

    def init_ui(self):
        self.canvas = tk.Canvas(self.root, width=GRID_SIZE * (CELL_SIZE + GAP) + GAP, 
                                height=GRID_SIZE * (CELL_SIZE + GAP) + GAP, bg=BACKGROUND_COLOR)
        self.canvas.pack()
        self.root.bind("<KeyPress>", self.handle_keypress)

    def spawn_tile(self):
        empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.board[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.board[r][c] = 2 if random.random() < 0.9 else 4

    def update_ui(self):
        self.canvas.delete("all")
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x, y = c * (CELL_SIZE + GAP) + GAP, r * (CELL_SIZE + GAP) + GAP
                value = self.board[r][c]
                color = TILE_COLORS.get(value, EMPTY_CELL_COLOR)
                self.canvas.create_rectangle(x, y, x + CELL_SIZE, y + CELL_SIZE, fill=color, outline="")
                if value:
                    self.canvas.create_text(x + CELL_SIZE // 2, y + CELL_SIZE // 2, text=str(value), font=FONT, fill="#776e65")

    def handle_keypress(self, event):
        key_map = {"Up": self.move_up, "Down": self.move_down, "Left": self.move_left, "Right": self.move_right}
        if event.keysym in key_map:
            key_map[event.keysym]()
            self.spawn_tile()
            self.update_ui()

    def compress(self, row):
        new_row = [num for num in row if num != 0]
        new_row += [0] * (GRID_SIZE - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(GRID_SIZE - 1):
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2
                row[i + 1] = 0
        return row

    def move_left(self):
        for r in range(GRID_SIZE):
            self.board[r] = self.compress(self.merge(self.compress(self.board[r])))

    def move_right(self):
        for r in range(GRID_SIZE):
            self.board[r] = list(reversed(self.compress(self.merge(self.compress(reversed(self.board[r]))))))

    def move_up(self):
        self.board = list(map(list, zip(*self.board)))
        self.move_left()
        self.board = list(map(list, zip(*self.board)))

    def move_down(self):
        self.board = list(map(list, zip(*self.board)))
        self.move_right()
        self.board = list(map(list, zip(*self.board)))

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
