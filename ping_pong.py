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
import json

WIDTH = 800
HEIGHT = 600
# The below should be in the same path where this pingpong.py file is run
FILE = "config.json"

CONFIG = None
if os.path.isfile(FILE):
    CONFIG = json.load(open('config.json'))
else:
    raise FileNotFoundError("The configuration file is missing or not found.")

GAME_SPEED = float(CONFIG['game_speed'])

WINDOW = turtle.Screen()
WINDOW.title("Ping Pong Game by @PrinceNyeche")
WINDOW.bgcolor("black")
WINDOW.setup(width=WIDTH, height=HEIGHT)
WINDOW.tracer(0)

# Paddle A
PADDLE_A = turtle.Turtle()
PADDLE_A.speed(0)
PADDLE_A.shape("square")
PADDLE_A.color("white")
PADDLE_A.shapesize(stretch_wid=5, stretch_len=1)
PADDLE_A.penup()
PADDLE_A.goto(-350, 0)

# Paddle B
PADDLE_B = turtle.Turtle()
PADDLE_B.speed(0)
PADDLE_B.shape("square")
PADDLE_B.color("white")
PADDLE_B.shapesize(stretch_wid=5, stretch_len=1)
PADDLE_B.penup()
PADDLE_B.goto(350, 0)

# Ball
BALL = turtle.Turtle()
BALL.speed(GAME_SPEED)
BALL.shape("circle")
BALL.color("white")
BALL.penup()
BALL.goto(0, 0)
BALL.dx = 2
BALL.dy = -2

# Pen
PEN = turtle.Turtle()
PEN.speed(0)
PEN.color("white")
PEN.penup()
PEN.hideturtle()
PEN.goto(0, 260)
PEN.write(f"{CONFIG['player_name_one']}: 0 {CONFIG['player_name_two']}: 0",
          align="center", font=("Courier", 24, "normal"))


# automated user
# Player A or B or CPU
def cpu(attr: bool = True) -> None:
    """An automated cpu user.

    :param attr: Switches context between left and right
     paddle

    :return: None
    """
    # get the ball position and compare coordinates
    get_ball = BALL.pos()
    ball_cord = BALL.xcor(), BALL.ycor()

    def movement():
        # define the speed for paddle of cpu user 0=fastest, 1=slowest
        content = PADDLE_A if attr is True else PADDLE_B
        content.speed(CONFIG['menu']['speed'])
        y_axis = ball_cord > (10, 50) if attr is \
                                         True else ball_cord > (30, -30)
        x_axis = ball_cord < (-50, -10) if attr is \
                                           True else ball_cord < (-30, -60)
        player = CONFIG['player_name_one'] \
            if attr is True else CONFIG['player_name_two']
        if get_ball:
            # get ball/paddle collision
            values = -340 > BALL.xcor() > -350 if attr is True else \
                340 < BALL.xcor() < 350
            if values and (content.ycor() + 50
                           > BALL.ycor() > content.ycor() - 50):
                BALL.dx *= -1
                sound_on()

            # Look at the y-axis right-side
            if y_axis:
                my_value = 50 if attr is True else 180
                if content.towards(get_ball) < my_value:
                    paddle_a_up() if attr is \
                                     True else paddle_b_up()
                    print(f"{player}: moving up")
                else:
                    if attr is False:
                        if content.towards(get_ball) > 20:
                            paddle_b_down()
                            print(f"{player}: moving down")
                            # Look at the x-axis right-side
            elif x_axis:
                symbol = content.towards(get_ball) < 150 if attr is False \
                    else content.towards(get_ball) > 100
                if symbol:
                    (paddle_a_up() if attr is True else paddle_b_up()) \
                        if attr is False else \
                        (paddle_a_down() if attr is True else paddle_b_down())
                    print("{}: {}".format(player, "moving up"
                    if attr is False else "moving down"))
                else:
                    if attr is True:
                        # correct movement along this axis
                        if content.towards(get_ball) < 50:
                            paddle_a_up()
                            print(f"{player}: moving up")

    movement()


# button control functions
def paddle_a_up():
    y = PADDLE_A.ycor()
    y += 20
    PADDLE_A.sety(y)


def paddle_a_down():
    y = PADDLE_A.ycor()
    y -= 20
    PADDLE_A.sety(y)


def paddle_b_up():
    y = PADDLE_B.ycor()
    y += 20
    PADDLE_B.sety(y)


def paddle_b_down():
    y = PADDLE_B.ycor()
    y -= 20
    PADDLE_B.sety(y)


# keyboard binding
WINDOW.listen()
WINDOW.onkeypress(paddle_a_up, "w")
WINDOW.onkeypress(paddle_a_down, "s")
WINDOW.onkeypress(paddle_b_up, "Up")
WINDOW.onkeypress(paddle_b_down, "Down")


# a function to always play sound no matter the platform
def system_sound(sound: str = None):
    """Creates audio sound"""
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


def sound_on():
    """Enabling sound"""
    system_sound("sounds/bounce.wav") \
        if CONFIG["sound"] == "on".lower() else None


def main():
    # Scoreboard
    score_a = 0
    score_b = 0
    global GAME_SPEED
    keep_score_track_a, keep_score_track_b = score_a, score_b
    idle_time = 0
    while True:
        WINDOW.update()

        # move the ball
        BALL.setx(BALL.xcor() + BALL.dx)
        BALL.sety(BALL.ycor() + BALL.dy)

        def speed_up():
            # Paddle and ball collision
            global GAME_SPEED
            GAME_SPEED -= 0.001
            BALL.speed(GAME_SPEED)
            if idle_time == 15:
                # This overrides the ball_speed_limit for the first time only
                BALL.dx *= CONFIG["ball_speed"]
            else:
                BALL.dx *= -1.1 if BALL.dx < \
                                   abs(CONFIG['ball_speed_limit']) else -1

        # boarder checking for ball then make sound
        # top
        if BALL.ycor() > 290:
            BALL.sety(290)
            BALL.dy *= -1
            sound_on()

        # bottom
        elif BALL.ycor() < -290:
            BALL.sety(-290)
            BALL.dy *= -1
            sound_on()

        # right
        if BALL.xcor() > 390:
            score_a += 1
            PEN.clear()
            PEN.write(f"{CONFIG['player_name_one']}: {score_a} "
                      f"{CONFIG['player_name_two']}: {score_b}",
                      align="center", font=("Courier", 24, "normal"))
            BALL.goto(0, 0)
            speed_up()

        # left
        elif BALL.xcor() < -390:
            score_b += 1
            PEN.clear()
            PEN.write(f"{CONFIG['player_name_one']}: {score_a} "
                      f"{CONFIG['player_name_two']}: {score_b}",
                      align="center", font=("Courier", 24, "normal"))
            BALL.goto(0, 0)
            speed_up()

        if CONFIG["menu"]:
            # change the menu->player_one=robot for cpu user
            if CONFIG["menu"]["player_one"] == "robot".lower():
                keep_score_track_a = score_a
                cpu(True)
            if CONFIG["menu"]["player_two"] == "robot".lower():
                keep_score_track_b = score_b
                cpu(False)

            if CONFIG["menu"]["player_one"] != "robot".lower():
                # first player left paddle if menu->player_one=human
                # in config file
                # "WS" keyboard use "w" for up, "s" for down
                if (-340 > BALL.xcor() > -350) and \
                        (PADDLE_A.ycor() + 50 >
                         BALL.ycor() > PADDLE_A.ycor() - 50):
                    BALL.dx *= -1
                    sound_on()
            if CONFIG["menu"]["player_two"] != "robot".lower():
                # second player right paddle if menu->player_two=human
                # in config file
                # "up/down arrow keys" keyboard use "up" for up,
                # "down" for down
                if (340 < BALL.xcor() < 350) and \
                        (PADDLE_B.ycor() + 50 > BALL.ycor()
                         > PADDLE_B.ycor() - 50):
                    BALL.dx *= -1
                    sound_on()

        auto_score = keep_score_track_a \
            if keep_score_track_a else keep_score_track_b \
            if keep_score_track_b else 0
        if auto_score >= CONFIG['score_limit']:
            WINDOW.bgcolor("black")
            PEN.clear()
            GAME_SPEED = 0.1
            PADDLE_A.goto(800, 800)
            PADDLE_B.goto(800, 800)
            BALL.goto(0, 0)
            BALL.hideturtle()
            PEN.write(f"{CONFIG['player_name_one']}: {score_a} "
                      f"{CONFIG['player_name_two']}: {score_b}",
                      align="center", font=("Courier", 24, "normal"))
            BALL.write("GAME OVER", align="center",
                       font=("Courier", 40, "normal"))

        if idle_time == 15:
            speed_up()

        idle_time += 1


if __name__ == "__main__":
    main()
    WINDOW.mainloop()
