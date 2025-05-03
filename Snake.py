from tkinter import *
import random

# Game settings
GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 70
SPACE_SIZE = 50
BODY_PARTS = 4
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class GameObject:
    def __init__(self, canvas, x, y, color, tag):
        self._canvas = canvas
        self._x = x
        self._y = y
        self._color = color
        self._tag = tag
        self._shape = None
        self.draw()

    def draw(self):
        raise NotImplementedError("Subclasses must implement draw()")

    def get_position(self):
        return [self._x, self._y]

    def delete(self):
        if self._shape:
            self._canvas.delete(self._shape)

class Food(GameObject):
    def __init__(self, canvas):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        super().__init__(canvas, x, y, FOOD_COLOR, "food")

    def draw(self):
        self._shape = self._canvas.create_oval(self._x, self._y,
                                               self._x + SPACE_SIZE, self._y + SPACE_SIZE,
                                               fill=self._color, tag="Food")

class Snake(GameObject):
    def __init__(self, canvas):
        self._canvas = canvas
        self._body_size = BODY_PARTS
        self._coordinates = [[0, 0] for _ in range(BODY_PARTS)]
        self._squares = []
        self._create_body()

    def _create_body(self):
        for x, y in self._coordinates:
            square = self._canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                                                   fill=SNAKE_COLOR, tag="snake")
            self._squares.append(square)

    def move(self, direction):
        x, y = self._coordinates[0]
        if direction == "up":
            y -= SPACE_SIZE
        elif direction == "down":
            y += SPACE_SIZE
        elif direction == "left":
            x -= SPACE_SIZE
        elif direction == "right":
            x += SPACE_SIZE

        self._coordinates.insert(0, [x, y])
        square = self._canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                                               fill=SNAKE_COLOR, tag="snake")
        self._squares.insert(0, square)

    def remove_tail(self):
        del self._coordinates[-1]
        self._canvas.delete(self._squares[-1])
        del self._squares[-1]

    def get_head_position(self):
        return self._coordinates[0]

    def get_body_positions(self):
        return self._coordinates[1:]

    def grow(self):
        pass

class SnakeGame:
    def __init__(self, window):
        self.window = window
        self.score = 0
        self.direction = 'down'
        self.canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
        self.label = Label(window, text="Score:0", font=('consolas', 40))
        self.label.pack()
        self.canvas.pack()

        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas)

        self._bind_keys()
        self._center_window()
        self._next_turn()

    def _bind_keys(self):
        self.window.bind('<Left>', lambda event: self._change_direction('left'))
        self.window.bind('<Right>', lambda event: self._change_direction('right'))
        self.window.bind('<Up>', lambda event: self._change_direction('up'))
        self.window.bind('<Down>', lambda event: self._change_direction('down'))

    def _center_window(self):
        self.window.update()
        w, h = self.window.winfo_width(), self.window.winfo_height()
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        x, y = int((sw - w) / 2), int((sh - h) / 2)
        self.window.geometry(f"{w}x{h}+{x}+{y}")

    def _change_direction(self, new_dir):
        opposites = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
        if new_dir != opposites.get(self.direction):
            self.direction = new_dir

    def _next_turn(self):
        self.snake.move(self.direction)
        x, y = self.snake.get_head_position()

        if [x, y] == self.food.get_position():
            self.score += 1
            self.label.config(text=f"Score:{self.score}")
            self.food.delete()
            self.food = Food(self.canvas)
        else:
            self.snake.remove_tail()

        if self._check_collisions():
            self._game_over()
        else:
            self.window.after(SPEED, self._next_turn)

    def _check_collisions(self):
        x, y = self.snake.get_head_position()
        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            return True
        if [x, y] in self.snake.get_body_positions():
            return True
        return False

    def _game_over(self):
        self.canvas.delete(ALL)
        self.canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2,
                                font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")

# Main setup
if __name__ == "__main__":
    root = Tk()
    root.title("Snake")
    root.resizable(False, False)
    game = SnakeGame(root)
    root.mainloop()
