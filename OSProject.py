import tkinter as tk
import random

# Constants
WIDTH, HEIGHT = 400, 600
BALL_RADIUS = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 80, 10
BRICK_WIDTH, BRICK_HEIGHT = 70, 40
BRICK_ROWS, BRICK_COLUMNS = 5, 8
BRICK_COLOR = ["red", "orange", "yellow", "green", "blue"]

# Initialize the tkinter window
root = tk.Tk()
root.title("Brick Breaker")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# Create the paddle
paddle = canvas.create_rectangle(
    WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - PADDLE_HEIGHT - 10,
    WIDTH // 2 + PADDLE_WIDTH // 2, HEIGHT - 10, fill="white"
)

# Initialize the ball
ball = canvas.create_oval(
    WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS,
    WIDTH // 2 + BALL_RADIUS, HEIGHT // 2 + BALL_RADIUS, fill="white"
)

# Initialize the bricks
bricks = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLUMNS):
        x1 = col * BRICK_WIDTH
        y1 = row * BRICK_HEIGHT
        x2 = x1 + BRICK_WIDTH
        y2 = y1 + BRICK_HEIGHT
        bricks.append(canvas.create_rectangle(x1, y1, x2, y2, fill=random.choice(BRICK_COLOR)))

# Initialize ball speed
ball_speed_x = 7
ball_speed_y = 7

# Initialize paddle speed
paddle_speed = 2

# Function to move the paddle
def move_paddle(event):
    global paddle_speed
    if event.keysym == "Left":
        paddle_speed = -10
    elif event.keysym == "Right":
        paddle_speed = 10

# Function to stop moving the paddle
def stop_paddle(event):
    global paddle_speed
    paddle_speed = 0
# Bind paddle movement to arrow keys
root.bind("<Left>", move_paddle)
root.bind("<Right>", move_paddle)
root.bind("<KeyRelease-Left>", stop_paddle)
root.bind("<KeyRelease-Right>", stop_paddle)

# Function to update the game
def update():
    global ball_speed_x, ball_speed_y

    # Move the ball
    canvas.move(ball, ball_speed_x, ball_speed_y)

    # Move the paddle
    canvas.move(paddle, paddle_speed, 0)

    # Get the current position of the ball
    ball_coords = canvas.coords(ball)

    # Detect collisions with the walls
    if ball_coords[0] <= 0 or ball_coords[2] >= WIDTH:
        ball_speed_x = -ball_speed_x

    if ball_coords[1] <= 0:
        ball_speed_y = -ball_speed_y

    # Detect collisions with the paddle
    if canvas.coords(ball)[3] >= canvas.coords(paddle)[1] and canvas.coords(ball)[2] >= canvas.coords(paddle)[0] and canvas.coords(ball)[0] <= canvas.coords(paddle)[2]:
        ball_speed_y = -ball_speed_y

    # Detect collisions with bricks
    for brick in bricks:
        brick_coords = canvas.coords(brick)
        if ball_coords[1] <= brick_coords[3] and ball_coords[3] >= brick_coords[1] and ball_coords[2] >= brick_coords[0] and ball_coords[0] <= brick_coords[2]:
            ball_speed_y = -ball_speed_y
            canvas.delete(brick)
            bricks.remove(brick)

    # Check if the player has won
    if len(bricks) == 0:
        canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Winner Winner,Chicken DINNER!", font=("Helvetica", 24), fill="white")
        root.update()
        return

    # Check if the player has lost
    if ball_coords[3] >= HEIGHT:
        canvas.create_text(WIDTH // 2, HEIGHT // 2, text="CHAL NIKAL!\n tere bas ki nhi!!!!", font=("Helvetica", 24), fill="white")
        root.update()
        return

    # Update the game after a delay
    root.after(30, update)

# Start the game loop
update()

# Start the tkinter main loop
root.mainloop()