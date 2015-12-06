# import the random library, to set the initial position of the rock.
import random

# Set the size of the window
WIDTH = 600
HEIGHT = 500

# Create the actors
spacecraft = Actor('spacecraft')    # The spacecraft actor
rock = Actor('rock') # Rock actor with the same image

# Create the laser rect
# (Not within the screen area.)
laser = Rect((0,-HEIGHT*4), (2, 1000))  

# The centre of the screen
centre_x = WIDTH/2
centre_y = HEIGHT/2

# Global flags
gameOver = False
laserCharged = True
laserFiring = False
rmRock = False

# The score
score = 0
topScore = 0
# ---------------------------------------

def startingPosition():
  # A random position along the top of the screen
  return (random.randint(0, WIDTH), 0)

# ---------------------------------------

def startingVelocity():
  # A random velocity, going downwards away from the top of the screen.
  return (random.randint(-5, 5), random.randint(1, 5))

# ---------------------------------------

def initialRockPosition():
  global rock
  global rock_vx
  global rock_vy
  global rmRock
  rock.image = 'rock' # In case it has been destroyed
  rock.pos = 0, HEIGHT*2 # Off the screen
  rock_vx = 0 # Set the x component of the rock velocity to be zero
  rock_vy = 0 # Set the y component of the rock velocity to be zero

  # Random starting position, along top edge.
  (rock.x, rock.y) = startingPosition() 

  # Random starting velocity, going down the screen
  (rock_vx, rock_vy) = startingVelocity() 

  # Set the rock to the default image, just in case it has been
  # destroyed.
  rock.image = 'rock'

  # Reset the rock removal flag, used by the clock to allow the rock
  # to be seen to be destroyed.
  rmRock = False

# ---------------------------------------

def initialPositions():
  global spacecraft
  global score
  spacecraft.image = 'spacecraft' # In case it has been destroyed
  # Initial position and velocity
  spacecraft.pos = centre_x, centre_y # Inital position of the spacecraft
  initialRockPosition()  # Set the initial rock position and image.
  score = 0 # Reset the score, since the game has just begun.

# ---------------------------------------

# Starting settings for the game
initialPositions()

# ---------------------------------------

# This function is called by the Pygame Zero timer
def laserFiringComplete():
  global laserFiring
  laserFiring = False # Set the firing flag, to show the laser beam

  # Use the clock to prevent the player from firing the laser straight
  # away.
  clock.schedule(laserChargingComplete, 1.0)

# ---------------------------------------

# This function is called by the Pygame Zero timer
def laserChargingComplete():
  global laserCharged
  # Set the charged flag, to allow the laser to be fired.
  laserCharged = True

# ---------------------------------------

# This function is called by the Pygame Zero timer
def removeRock():
  global rmRock
  # Set the rock removal flag, to make sure that the rock is removed.
  rmRock = True

# ---------------------------------------

def draw():
  global laser
  screen.clear()
  spacecraft.draw()
  rock.draw()

  # Draw the score information at the bottom of the screen.
  screen.draw.text("Score : "+str(score), center=(centre_x-100, HEIGHT-10.))
  screen.draw.text("Top Score : "+str(topScore), center=(centre_x+100, HEIGHT-10.))

  # If the laser is currently firing, then draw it.
  if laserFiring:
    screen.draw.filled_rect(laser,(0,255,0))

  # Check to see if the game is over
  if gameOver:
    # If the game is over, then print a series of red rectangles
    # with a text message.
    for i in range(20,-5,-5):
      screen.draw.filled_rect(Rect((centre_x-(100+i), centre_y-(30+i)), (200+(i*2), 80+(i*2))), (200-(i*8), 0, 0))
    screen.draw.text("GAME OVER!", center=(centre_x, centre_y))
    screen.draw.text("(n to restart)", center=(centre_x, centre_y+20))

# ---------------------------------------

def updateSpacecraft():
  global laserFiring
  global laserCharged
  global laser

  # If the cursor keys are pressed, then move the
  # spacecraft within the limits of the screen.
  if keyboard.left and spacecraft.left > 2:
    spacecraft.x -= 2
  if keyboard.right and spacecraft.right < WIDTH+2:
    spacecraft.x += 2
  if keyboard.down and spacecraft.bottom < HEIGHT+2:
    spacecraft.y += 2
  if keyboard.up and spacecraft.top > 2:
    spacecraft.y -= 2

  # If the spacebar has been pressed and the laser is charged, then
  # fire the laser.
  if keyboard.space and laserCharged:
    laserCharged = False
    laserFiring = True

    # The laser should fire for 3/10 of a second.
    clock.schedule(laserFiringComplete, 0.3)

  # If the laser is firing, then move it to where the spacecraft is.
  if laserFiring:
    laser = Rect((spacecraft.x-2,0),(4,spacecraft.top))

# ---------------------------------------

def updateRock():
  global rock

  # Check if the rock has gone off the screen or has been  If it has, then
  # reset its starting position and initial velocity.
  if rock.right < 0 or rock.left > WIDTH or rock.top > HEIGHT or rmRock:
    initialRockPosition()

  # Move the x position by the corresponding velocity component
  rock.x += rock_vx

  # Move the y position by the corresponding velocity component
  rock.y += rock_vy

# ---------------------------------------

def update():
  global gameOver
  global score
  global topScore

  # If the game is not over, move the spacecraft and rock
  if not gameOver:
    updateSpacecraft()
    updateRock()
  else:
    # If the game is over, test to see if the n key has been pressed.
    # If it has been pressed, reset the positions of the spracecraft and
    # rock and restart the game.
    if keyboard.n:
      initialPositions()
      gameOver = False

  # Check to see if the rock has collided with the spacecraft
  collision = spacecraft.colliderect(rock)

  # If there has been a collision, then switch both actors to their
  # destroyed versions and set the gameOver flag.
  if collision:
    rock.image = 'rock_destroyed'
    spacecraft.image = 'spacecraft_destroyed'
    gameOver = True
  
  # Check to see if the laser has hit the rock
  rockLaser = rock.colliderect(laser)

  # If the laser has hit the rock and the rock has not already been
  # destroyed, then destroy the rock and increment the score.
  if rockLaser and laserFiring and rock.image != 'rock_destroyed':
    rock.image = 'rock_destroyed'
    score = score + 1
    
    # If the current score is bigger than the top score, then update
    # the top score.
    if score > topScore:
      topScore = score

    # Set the timer to wait for a 1/5 of a second before removing the
    # destroyed rock from view.
    clock.schedule(removeRock, 0.2)
