import tkinter as tk
import random

# Constants
WIDTH = 800
HEIGHT = 600
SNAKE_SIZE = 10
SNAKE_SPEED = 100  

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='black')
        self.canvas.pack()

        self.start_screen()

    def start_screen(self):
        self.canvas.delete(tk.ALL)
        self.canvas.create_text(WIDTH // 2, HEIGHT // 3, text="Snake Game", fill="White", font=("Helvetica", 50, "bold"))
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Press Enter to Start", fill="white", font=("Helvetica", 30))
        self.canvas.create_text(WIDTH // 2, HEIGHT // 1.8, text="Use Arrow Keys to Move", fill="white", font=("Helvetica", 20))
        self.root.bind("<Return>", self.start_game)

    def start_game(self, event=None):
        self.root.unbind("<Return>")
        self.score = 0
        self.snake = [(WIDTH // 2, HEIGHT // 2)]
        self.snake_dir = 'Right'
        self.food = self.place_food()
        self.root.bind("<KeyPress>", self.on_key_press)
        self.update()

    def place_food(self):
        x = random.randint(0, (WIDTH // SNAKE_SIZE) - 1) * SNAKE_SIZE
        y = random.randint(0, (HEIGHT // SNAKE_SIZE) - 1) * SNAKE_SIZE
        return x, y

    def on_key_press(self, e):
        new_dir = e.keysym
        all_dirs = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if new_dir in all_dirs and new_dir != all_dirs[self.snake_dir]:
            self.snake_dir = new_dir

    def update(self):
        head_x, head_y = self.snake[0]

        if self.snake_dir == "Left":
            head_x -= SNAKE_SIZE
        elif self.snake_dir == "Right":
            head_x += SNAKE_SIZE
        elif self.snake_dir == "Up":
            head_y -= SNAKE_SIZE
        elif self.snake_dir == "Down":
            head_y += SNAKE_SIZE

        new_head = (head_x, head_y)
        self.snake = [new_head] + self.snake[:-1]

        if new_head in self.snake[1:] or head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            self.game_over()
            return

        if new_head == self.food:
            self.snake.append(self.snake[-1])
            self.food = self.place_food()
            self.score += 1

        self.draw()
        self.root.after(SNAKE_SPEED, self.update)

    def draw(self):
        self.canvas.delete(tk.ALL)
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + SNAKE_SIZE, segment[1] + SNAKE_SIZE, fill="White")
        self.canvas.create_oval(self.food[0], self.food[1], self.food[0] + SNAKE_SIZE, self.food[1] + SNAKE_SIZE, fill="red")
        self.canvas.create_text(50, 20, text=f"Score: {self.score}", fill="white", font=("Helvetica", 20, "bold"))

    def game_over(self):
        self.canvas.delete(tk.ALL)
        self.canvas.create_text(WIDTH // 2, HEIGHT // 3, text="GAME OVER", fill="red", font=("Helvetica", 50, "bold"))
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text=f"Score: {self.score}", fill="white", font=("Helvetica", 30))
        self.canvas.create_text(WIDTH // 2, HEIGHT // 1.5, text="Press Enter to Restart or Q to Quit", fill="white", font=("Helvetica", 20))
        self.root.bind("<Return>", self.start_game)
        self.root.bind("<KeyPress-q>", self.quit_game)

    def quit_game(self, event=None):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
