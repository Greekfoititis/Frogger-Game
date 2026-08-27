# The turtle library is used to render the river, road, and game components
import turtle
import math
import time
import random

# Create and setup the screen
t = turtle.Screen()
t.cv._rootwindow.resizable(False, False)  # Make the game window non-resizable
t.title("Frogger")
t.setup(600, 800)
t.bgcolor("white")
t.bgpic("background.gif")
t.tracer(0)  # Turn off automatic screen updates


# Register images with a for loop - loading shapes into the screen context
shapes = ["froggy.gif", "car1.gif", "car2.gif", "car3.gif", "log1.gif", "turtles2.gif",  "bike.gif","turtle.gif",
          "turtles3.gif",   "bus.gif",
          "home.gif", "goal.gif","tree1.gif","small_froggy.gif", "lives.gif", "one.gif",
          "two.gif", "three.gif", "time.gif", "tree2.gif", "30sec.gif", "40sec.gif"]

for shape in shapes:
    t.register_shape(shape)


# Initialize the turtle pen required for rendering with the turtle library
pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()
pen.color("white")
pen.penup()


# Base class definitions
class Gameobj(): # Base class of the program. All objects below inherit from this.    
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    def define(self, pen):  
        # Moves the pen cursor and stamps the image shape
        pen.goto(self.x, self.y)
        pen.shape(self.image)
        pen.stamp()

    def iscollision(self, other): # Checks if the frog is within collision distance of another object
        x_collision = (math.fabs(self.x - other.x) * 2) - (self.width + other.width) # fabs -> absolute value
        y_collision = (math.fabs(self.y - other.y) * 2) - (self.height + other.height)
        if x_collision < 0 and y_collision < 0:
            return (x_collision and y_collision)

    def update(self):
        pass

class Player(Gameobj):
    # Defines player/frog behavior and movement (e.g., 'Up' key moves 40 pixels up)
    def __init__(self, x, y, width, height, image):
        Gameobj.__init__(self, x, y, width, height, image) ## Class inheritance to reuse Gameobj methods
        self.dx = 0
        self.collision = False
        self.frogs_home = 0
        self.max_time = 40
        self.start_time = time.time()
        self.lives = 3
        
    def up(self):
        self.y += 40

    def down(self):
        self.y -= 40

    def right(self):
        self.x += 40

    def left(self):
        self.x -= 40
    
    def home(self):
        self.dx = 0
        self.x = 0
        self.y = -300
        self.max_time = 40
        self.start_time = time.time()        
        
    def update(self):
        self.x += self.dx
        
        # Check if the player moves out of screen bounds
        if self.x < -300 or self.x > 300:
            self.x = 0
            self.y = -300

        # Countdown timer logic: if inactive for 40 sec -> loses a life
        self.elapsed_time = time.time() - self.start_time
        print(self.max_time - int(self.elapsed_time))

        if self.elapsed_time > self.max_time:
            player.lives -= 1
            self.home()
        
class Car(Gameobj):
    # Car class - position and movement logic. When a car moves past the window edge, it wraps around to the other side.
    def __init__(self, x, y, width, height, image, dx):
        Gameobj.__init__(self, x, y, width, height, image)
        self.dx = dx

    def update(self):
        self.x += self.dx

        # Check if car goes off-screen
        if self.x < -350:
            self.x = 350

        if self.x > 350:
            self.x = -350
        

class Log(Gameobj):
     # Log class - position and movement logic for floating log platforms
    def __init__(self, x, y, width, height, image, dx):
        Gameobj.__init__(self, x, y, width, height, image)
        self.dx = dx

    def update(self):
        self.x += self.dx

        if self.x < -400:
            self.x = 400

        if self.x > 400:
            self.x = -400


class Turtles(Gameobj):
    # Defines turtle platform behavior in the river (speed, position, state)
    
    def __init__(self, x, y, width, height, image, dx):
        Gameobj.__init__(self, x, y, width, height, image)
        self.dx = dx
        self.state = "full"  
        self.full_time = 8
        self.half_time = 5
        self.submerged_time = 3
        self.start_time = time.time()

    def update(self):
        self.x += self.dx

        if self.x < -400:
            self.x = 400

        if self.x > 400:
            self.x = -400
        
           
class Goal(Gameobj):
    # Goal class - when the frog reaches a target home spot, it resets back to the starting position
    def __init__(self, x, y, width, height, image):
        Gameobj.__init__(self, x, y, width, height, image) 
        self.dx = 0

# Game Objects Initialization
player = Player(0, -300, 50, 50, "froggy.gif") # Player instance
player.define(pen) # Renders the frog at its default starting position 


level_1 = [Car(0, -135, 65, 20, "car1.gif", 2), Car(0, -215, 50, 20, "car3.gif", -1.5), # Initial positions of cars, turtles, logs, and static obstacles
           Car(0, -255, 50, 20, "car2.gif", 1.7), Car(0,-95, 75, 20, "bus.gif", -1.4),
           Car(-320, -255, 50, 20, "car2.gif", 1.7), Log(-350, 95, 105, 20, "log1.gif", -1.3),
           Car(0,-175, 40, 20, "bike.gif", 1.9), Log(0, 55, 105, 20, "log1.gif", 1.1),
           Log(0, 95, 105, 20, "log1.gif", -1.3), Log(0, 135, 105, 20, "log1.gif", 1.2),
           Turtles(0, 175, 10, 20, "turtle.gif", -2), Turtles(0, 255, 60, 20, "turtles2.gif", -1.8),
           Turtles(0, 215, 110, 20, "turtles3.gif", 1.5), Goal(80, 0, 30, 20, "tree1.gif"),
           Goal(-215, 10, 70, 40, "tree2.gif"), Turtles(-300, 175, 10, 20, "turtle.gif", -2),
           Turtles(-280, 255, 60, 20, "turtles2.gif", -1.8), Turtles(-250, 215, 110, 20, "turtles3.gif", 1.5),
           Log(-350, 55, 105, 20, "log1.gif", 1.1)]

homes = [Goal(0, 315, 50, 20 ,"home.gif"), Goal(-100, 315, 50, 20 ,"home.gif"),
         Goal(-200, 315, 50, 20 ,"home.gif"), Goal(100, 315, 50, 20 ,"home.gif"),
         Goal(200, 315, 50, 20 ,"home.gif")]



objects = level_1 + homes  # Combine all obstacles, decorative elements, and top home slots into one list
objects.append(player)


# Keyboard Bindings - Map keypresses to call corresponding player movement methods
t.listen()
t.onkeypress(player.up, "Up")
t.onkeypress(player.down, "Down")
t.onkeypress(player.right, "Right")
t.onkeypress(player.left, "Left")

while True:
    # Render and update all objects in each frame iteration
    for obj in objects:
        obj.define(pen)
        obj.update()

    # Display remaining lives icons on the bottom screen area
    pen.goto(-200, -325)
    pen.shape("small_froggy.gif")
    for life in range(player.lives):
        pen.goto(-285 + (life*30), -325)
        pen.stamp()
        print("Player lives:{}".format(player.lives))
        continue
        
    # Render time and lives UI indicators at the top of the screen
    pen.goto(-250, 375)
    pen.shape("lives.gif")
    pen.stamp()
    pen.goto(-205, 373)
    if player.lives == 3:
        pen.shape("three.gif")
        pen.stamp()
    elif player.lives == 2:
        pen.shape("two.gif")
        pen.stamp()
    elif player.lives == 1:
        pen.shape("one.gif")
        pen.stamp()
    else:
        pen.shape("lives.gif")
        pen.stamp()
    pen.goto(210,370)
    pen.shape("time.gif")
    pen.stamp()

    # Collision detection logic - subtract a life or attach player to floating platforms
    player.dx = 0
    player.collision = False
    for obj in objects:
        if player.iscollision(obj):
            if isinstance(obj, Car):
                player.lives -= 1
                player.home()
                break
            elif isinstance(obj, Log):
                player.dx = obj.dx
                player.collision = True
                break
            elif isinstance(obj, Turtles) and obj.state != "submerged":
                player.dx = obj.dx
                player.collision = True
                break
            elif isinstance(obj, Goal):
                if obj in homes:
                    if "goal.gif" == True:
                        player.frogs_home = player.frogs_home
                        player.y -= 40
                    else:
                        player.home()
                        obj.image = "goal.gif"
                        player.frogs_home += 1
                elif obj in level_1:
                    if player.x < obj.x :
                        player.x -= 40
                        #player.y = player.y
                        break
                    elif player.x > obj.x :
                        player.x += 40
                        #player.y = player.y
                        break
                    elif player.y < obj.y:
                        player.y -= 40
                    else:
                        player.y += 40

    # Water hazard & timeout logic - losing a life if drowning or remaining in water without platform
    if player.y > 40 and player.collision != True:
        player.lives -= 1
        player.home()
    if player.frogs_home < 3:
        pen.goto(255, 370)
        pen.shape("40sec.gif")
        pen.stamp()
    else:
        pen.goto(255, 370)
        pen.shape("30sec.gif")
        pen.stamp()
    if player.y < -300:
        player.x = player.x
        player.y += 40

    # Game win condition (all 5 homes reached) - reset homes and lives
    if player.frogs_home == 5:
        player.home
        player.frogs_home = 0
        player.lives = 3
        for home in homes:
            home.image = "home.gif"

    # Game over condition (0 lives left) - reset game state
    if player.lives == 0:
        player.home()
        player.frogs_home = 0
        for home in homes:
            home.image = "home.gif"
        player.lives = 3

    # Increase difficulty when 3 goals are completed (timer drops to 30 sec)
    if player.frogs_home == 3:
        player.max_time = 30
        
                
    t.update()  # Refresh the screen frame
    pen.clear() # Clear pen drawings to prepare for the next frame render cycle
 

t.mainloop()
