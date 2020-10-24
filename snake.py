"""
Game: Snake
License: MIT License
Author: Prince Nyeche
                 _
                | |
 ___ _ __   __ _| | _____
/ __| '_ \ / _` | |/ / _ \
\__ \ | | | (_| |   <  __/
|___/_| |_|\__,_|_|\_\___|

A Snake Game made on Python 3.7 with Turtle Module
"""

import turtle
import time
import os
import platform
from random import randint

# Our Screen
window = turtle.Screen()
window.title("A Snake Game by @PrinceNyeche")
window.setup(width=600, height=600)
window.bgcolor("blue")
window.tracer(0)

# Our Food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")  # start with red
food.shapesize(0.50, 0.50)
food.penup()
# so we used a random way to display the food
# x -270 to +220 px from the left to right
# y -270 to +220 px from the bottom to top
x, y = randint(-270, 220), randint(-270, 220)
food.goto(x, y)

# displays Scores
score = turtle.Turtle()
score.speed(0)
score.color("white")
score.penup()
score.hideturtle()
score.goto(260, 270)
score.write("Score: 0", align="right", font=("Courier", 20, "normal"))

# displays high score
high_score = turtle.Turtle()
high_score.speed(0)
high_score.color("white")
high_score.penup()
high_score.hideturtle()
high_score.goto(-290, 270)
high_score.write("High Score:  0", align="left", font=("Courier", 20, "normal"))

# displays snake life
lives = turtle.Turtle()
lives.speed(0)
lives.color("white")
lives.penup()
lives.hideturtle()
lives.goto(0, 270)
lives.write("Life: 3", align="center", font=("Courier", 20, "normal"))

# Player Snake
snake = turtle.Turtle()
snake.speed(0)
snake.shape("square")
snake.color("white")
snake.penup()
snake.goto(0, 0)
# move our snake head
snake.head = "wait"


# snake movement
def movement():
    if snake.head == "up":
        cy = snake.ycor()
        cy += 10
        snake.sety(cy)

    elif snake.head == "down":
        cy = snake.ycor()
        cy -= 10
        snake.sety(cy)

    elif snake.head == "left":
        # left movement
        cy = snake.xcor()
        cy -= 10
        snake.setx(cy)

    elif snake.head == "right":
        # right movement
        cy = snake.xcor()
        cy += 10
        snake.setx(cy)


# direction binding
def turn_up():
    if snake.head != "down":
        snake.head = "up"


def turn_down():
    if snake.head != "up":
        snake.head = "down"


def turn_left():
    if snake.head != "right":
        snake.head = "left"


def turn_right():
    if snake.head != "left":
        snake.head = "right"


# this basically just stops the head from moving
# press the "Enter" key
def pause_game():
    snake.head = "wait"


# keyboard binding
# use the Arrow keys to Control the snake
window.listen()
window.onkeypress(turn_up, key="Up")
window.onkeypress(turn_down, key="Down")
window.onkeypress(turn_left, key="Left")
window.onkeypress(turn_right, key="Right")
window.onkeypress(pause_game, key="Return")


# main game loop
def main():
    high_score_count = 0
    score_count = 0
    life = 3
    game_speed = 0.1
    # foods colors
    pick_ups = ["red", "yellow", "black", "green"]
    snake_body = []

    while True:

        window.update()
        time.sleep(game_speed)

        def hide_snake(n: int = 0, m: int = 0):
            # hide the snake from screen
            for each_body in snake_body:
                each_body.goto(n, m)

            snake_body.clear()

        # a function to always play sound no matter the platform
        def system_sound(sound: str = None):
            if platform.system() == "Darwin":
                if sound is not None:
                    return os.system(f"afplay {sound}&")
            if platform.system() == "Linux":
                if sound is not None:
                    return os.system(f"aplay {sound}&")
            if platform.system() == "Windows":
                import winsound
                if sound is not None:
                    return winsound.PlaySound(sound, winsound.SND_ASYNC)

        # boarder checking for Player snake
        if snake.ycor() > 280 or snake.ycor() < -270 or snake.xcor() < -280 or snake.xcor() > 270:
            system_sound("sounds/hitwall.wav")
            time.sleep(1)
            score.clear()
            high_score.clear()
            lives.clear()

            snake.goto(0, 0)
            snake.head = "wait"

            # hide the snake from screen
            hide_snake(500, 500)
            life -= 1

            # reset the score and game speed
            score_count = 0
            game_speed = 0.1

            high_score.write(f"High Score:  {high_score_count}", align="left", font=("Courier", 20, "normal"))
            score.write(f"Score: {score_count}", align="right", font=("Courier", 20, "normal"))
            lives.write(f"Life: {life}", align="center", font=("Courier", 20, "normal"))

        # add the body collision with itself
        for this_body in snake_body:
            if snake.position() == this_body.position():
                # let's make a sound on collision
                system_sound("sounds/hitwall.wav")
                time.sleep(1)
                score.clear()
                high_score.clear()
                lives.clear()
                hide_snake(590, 590)
                snake.goto(0, 0)
                snake.head = "wait"

                life -= 1

                # reset the score and game speed
                score_count = 0
                game_speed = 0.1

                high_score.write(f"High Score:  {high_score_count}", align="left", font=("Courier", 20, "normal"))
                score.write(f"Score: {score_count}", align="right", font=("Courier", 20, "normal"))
                lives.write(f"Life: {life}", align="center", font=("Courier", 20, "normal"))

        # get the position of the food
        if snake.distance(food) < 20:
            # play a sound each time food is eaten
            system_sound("sounds/chew.wav")
            a, b = randint(-270, 220), randint(-270, 220)
            # random food
            i = pick_ups[randint(0, 3)]
            food.color(i)
            food.goto(a, b)

            # define and call the new body
            new_snake_body = turtle.Turtle()
            new_snake_body.speed(0)
            new_snake_body.shape("square")
            new_snake_body.penup()
            new_snake_body.color("orange")
            snake_body.append(new_snake_body)

            # give a score
            score.clear()
            score_count += 5

            # gradually increase the game speed
            game_speed -= 0.001

            # update scores
            if score_count > high_score_count:
                high_score_count = score_count

            score.write(f"Score: {score_count}", align="right", font=("Courier", 20, "normal"))

        # make sure that our snake head is always there
        if len(snake_body) > 0:
            cx_body = snake.xcor()
            cy_body = snake.ycor()
            snake_body[0].goto(cx_body, cy_body)

            # reset the game speed
            game_speed = 0.1

            # food eaten, add a new body to the snake body
            for find_body in range(len(snake_body) - 1, 0, -1):
                x_body = snake_body[find_body - 1].xcor()
                y_body = snake_body[find_body - 1].ycor()
                snake_body[find_body].goto(x_body, y_body)
                game_speed -= 0.001

        if life < 1:
            # makes an awful sound if allowed system_sound("sounds/gameover.wav")
            food.goto(600, 600)
            hide_snake(590, 590)
            window.bgcolor("black")
            snake.goto(0, 0)
            snake.head = "wait"
            high_score.goto(0, -120)
            snake.hideturtle()
            snake.write(f"GAME OVER", align="center", font=("Courier", 40, "normal"))
            high_score.write(f"High Score: {high_score_count}", align="center",
                             font=("Courier", 20, "normal"))

        movement()


if __name__ == '__main__':
    main()
    window.mainloop()
