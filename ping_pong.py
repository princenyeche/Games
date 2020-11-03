"""
Game: Ping Pong
License: MIT License
Author: Prince Nyeche
       _
      (_)
 _ __  _ _ __   __ _ _ __   ___  _ __   __ _
| '_ \| | '_ \ / _` | '_ \ / _ \| '_ \ / _` |
| |_) | | | | | (_| | |_) | (_) | | | | (_| |
| .__/|_|_| |_|\__, | .__/ \___/|_| |_|\__, |
| |             __/ | |                 __/ |
|_|            |___/|_|                |___/

A Ping Pong Game made on Python 3.7
"""
import turtle
import platform
import os


window = turtle.Screen()
window.title("Ping Pong Game by @PrinceNyeche")
window.bgcolor("black")
window.setup(width=800, height=600)
window.tracer(0)

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 2
ball.dy = -2

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0 Player B: 0", align="center", font=("Courier", 24, "normal"))

# an automated player
cpu = turtle.Turtle()
cpu.speed(0)


# TODO: automated user
# Player A -> CPU
def player_cpu():
    pass


# functions
def paddle_a_up():
    y = paddle_a.ycor()
    y += 20
    paddle_a.sety(y)


def paddle_a_down():
    y = paddle_a.ycor()
    y -= 20
    paddle_a.sety(y)


def paddle_b_up():
    y = paddle_b.ycor()
    y += 20
    paddle_b.sety(y)


def paddle_b_down():
    y = paddle_b.ycor()
    y -= 20
    paddle_b.sety(y)


# keyboard binding
window.listen()
window.onkeypress(paddle_a_up, "w")
window.onkeypress(paddle_a_down, "s")
window.onkeypress(paddle_b_up, "Up")
window.onkeypress(paddle_b_down, "Down")


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


def main():
    # Score
    score_a = 0
    score_b = 0
    while True:
        window.update()

        # move the ball
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # TODO: pending creation of cpu player
        # cpu player
        # player_cpu()

        # boarder checking for ball
        # top
        if ball.ycor() > 290:
            ball.sety(290)
            ball.dy *= -1
            system_sound("sounds/bounce.wav")

        # bottom
        elif ball.ycor() < -290:
            ball.sety(-290)
            ball.dy *= -1
            system_sound("sounds/bounce.wav")

        # right
        if ball.xcor() > 390:
            score_a += 1
            pen.clear()
            pen.write(f"Player A: {score_a} Player B: {score_b}",
                      align="center", font=("Courier", 24, "normal"))
            ball.goto(0, 0)
            ball.dx *= -1

        # left
        elif ball.xcor() < -390:
            score_b += 1
            pen.clear()
            pen.write(f"Player A: {score_a} Player B: {score_b}",
                      align="center", font=("Courier", 24, "normal"))
            ball.goto(0, 0)
            ball.dx *= -1

        # Paddle and ball collision
        # right paddle
        if (340 < ball.xcor() < 350) and (paddle_b.ycor() + 50 > ball.ycor() > paddle_b.ycor() - 50):
            ball.dx *= -1
            system_sound("sounds/bounce.wav")

        # left paddle
        elif (-340 > ball.xcor() > -350) and (paddle_a.ycor() + 50 > ball.ycor() > paddle_a.ycor() - 50):
            ball.dx *= -1
            system_sound("sounds/bounce.wav")


if __name__ == "__main__":
    main()
    window.mainloop()
