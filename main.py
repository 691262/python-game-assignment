"""
Quiz program
"""

import random
import arcade
import math
import os
import sys
import time

QUIZ_QUESTIONS = 4

SPRITE_SCALING_PLAYER = 1
SPRITE_SCALING_COIN = 0.5
SPRITE_SCALING_LASER = 1
COIN_COUNT = 20

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Quiz game"

BULLET_SPEED = 20
MOVEMENT_SPEED = 5

#image files
coinImg = "images/cloud.png"
playerImg = "images/jet.png"
laserImg = "images/missile.png"

#sound files
jumpSnd = "sounds/jump.wav"
laserSnd = "sounds/laser.wav"

window = None

quizScore = 0
question = None
questionPos = 0

print("This is a quiz game. Collect all the coins to get the question\n\nHistory of programming languages")

def Quiz():
    global quizScore
    global question
    global questionPos

    #possible answers. alt answers are for questions with more than 1 answer
    questionAnswer = 0
    altAnswer1 = 0
    altAnswer2 = 0

    def IntCheck(msg):
        while True:
            try:
                number = int(input(msg))
                if number < 0 or number > 4:
                    raise
                break

            except ValueError:
                print("Not a number")
            except KeyboardInterrupt:
                print("\nEnd")
                sys.exit(0)
            except:
                print("Not a valid number")
        return number
    
    if questionPos == 0:
        question = ("Question 1: What was one of the first programming language\n"
                    "1. FORTAN\n"
                    "2. BASIC\n"
                    "3. C\n"
                    "4. LISP\n"
                    ">")
        questionAnswer = 1
    elif questionPos == 1:
        question = ("Question 2: What are some of the languages that were created in the 1960s to 1970s\n"
                    "1. SQL\n"
                    "2. Ada\n"
                    "3. C\n"
                    "4. Pascal\n"
                    "you might need to enter your input multiple times\n"
                    ">")
        questionAnswer = 1
        altAnswer1 = 4
        altAnswer2 = 3
    elif questionPos == 2:
        question = ("Question 3: What is a language that is used on websites\n"
                    "1. Python\n"
                    "2. Javascript\n"
                    "3. PHP\n"
                    "4. Ruby\n"
                    ">")
        questionAnswer = 2
        altAnswer1 = 3
    elif questionPos == 3:
        question = ("Question 4: Which one of these programming languages is object oriented\n"
                    "1. Java\n"
                    "2. Python\n"
                    "3. C\n"
                    "4. SQL\n"
                    ">")
        questionAnswer = 1
        altAnswer1 = 2

    answer = IntCheck(question)

    if answer == questionAnswer or answer == altAnswer1 or answer == altAnswer2:
        quizScore+=1
        questionPos+=1
        altAnswer1 = 0
        altAnswer2 = 0
        print("Correct. Score: ", int(quizScore))
    else:
        if questionPos == 1:
            print("Incorrect. The answer is", questionAnswer, ",", altAnswer1, "or", altAnswer2)
        elif questionPos == 2 or questionPos == 3:
            print("Incorrect. The answer is", questionAnswer, "or", altAnswer1)
        else:
            print("Incorrect. The answer is", questionAnswer)
            
        altAnswer1 = 0
        altAnswer2 = 0
        questionPos+=1


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        global jumpSnd
        global laserSnd

        # Variables that will hold sprite lists
        self.player_list = None
        self.coin_list = None
        self.bullet_list = None
        self.text_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        # Load sounds. Sounds from kenney.nl
        self.gun_sound = arcade.sound.load_sound(laserSnd)
        self.hit_sound = arcade.sound.load_sound(jumpSnd)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):

        """ Set up the game and initialize the variables. """

        global playerImg
        global coinImg
        global laserImg

        self.score = 0

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        # Image from kenney.nl
        self.player_sprite = arcade.Sprite(playerImg, SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = random.randrange(SCREEN_WIDTH)
        self.player_sprite.center_y = random.randrange(SCREEN_HEIGHT)
        self.player_list.append(self.player_sprite)

        # Create the coins
        for i in range(COIN_COUNT):
            coin = arcade.Sprite(coinImg, SPRITE_SCALING_COIN)

            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            self.coin_list.append(coin)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.coin_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse moves.
        """
        # Create a bullet
        bullet = arcade.Sprite(laserImg, SPRITE_SCALING_LASER)
        self.gun_sound.play(0.5)

        # Position the bullet at the player's current location
        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y

        # Get from the mouse the destination location for the bullet
        # IMPORTANT! If you have a scrolling screen, you will also need
        # to add in self.view_bottom and self.view_left.
        dest_x = x
        dest_y = y

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Angle the bullet sprite so it doesn't look like it is flying
        # sideways.
        bullet.angle = math.degrees(angle)
        #print(f"Bullet angle: {bullet.angle:.2f}")

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        bullet.change_x = math.cos(angle) * BULLET_SPEED
        bullet.change_y = math.sin(angle) * BULLET_SPEED

        # Add the bullet to the appropriate lists
        self.bullet_list.append(bullet)

    def on_update(self, delta_time):
        """ Movement and game logic """
        global question
        global questionPos
            
        # Call update on all sprites
        self.bullet_list.update()
        self.player_list.update()
        
        # Loop through each bullet
        for bullet in self.bullet_list:

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(bullet, self.coin_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
                arcade.play_sound(self.hit_sound)

            # For every coin we hit, add to the score and remove the coin
            for coin in hit_list:
                coin.remove_from_sprite_lists()
                self.score = self.score + 1
                #print("score:", self.score)
                if self.score == COIN_COUNT:
                    Quiz()
                    if questionPos == QUIZ_QUESTIONS:
                        print("Your score is", quizScore,"/", QUIZ_QUESTIONS)
                        self.close()
                    else:
                        self.setup()
                        self.activate()

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > self.width or bullet.top < 0 or bullet.right < 0 or bullet.left > self.width:
                bullet.remove_from_sprite_lists()

    def on_key_press(self, key, modifiers):
        #Movement inputs
        if key == arcade.key.W:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED
        #Other inputs
        elif key == arcade.key.ESCAPE:
            self.score = 0
            self.setup()
        elif key == arcade.key.END:
            self.close()

    def on_key_release(self, key, modifiers):
        #Movement release
        if key == arcade.key.W or arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or arcade.key.D:
            self.player_sprite.change_x = 0
           


def main():
    game = MyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
