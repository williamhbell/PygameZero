# import the random library, to set the initial position of the rock.
import random

# Set the size of the window
WIDTH = 600
HEIGHT = 500

# Create the actors
spacecraft = Actor('spacecraft')    # The spacecraft actor
rock = Actor('rock') # Rock actor with the same image

# Calculate the centre of the screen, to avoid doing so several
# times later on
centre_x = WIDTH/2
centre_y = HEIGHT/2

# ---------------------------------------

def initialPositions():
  global spacecraft
  global rock
  global rock_vx
  global rock_vy
  spacecraft.image = 'spacecraft' # In case it has been destroyed

  # Initial position and velocity
  spacecraft.pos = centre_x, centre_y # Inital position of the spacecraft
  rock.pos = 0, HEIGHT*2 # Off the screen
  rock_vx = 0 # Zero the x component of the rock velocity
  rock_vy = 0 # Zero the y component of the rock velocity

# ---------------------------------------

# Starting settings for the game
gameOver = False # The game has not finished yet
initialPositions() # Set the initial positions of the spacecraft and rock

# ---------------------------------------

def startingPosition():
  # A random position along the top of the screen
  return (random.randint(0, WIDTH), 0)

# ---------------------------------------

def startingVelocity():
  # A random velocity, going downwards away from the top of the screen.
  return (random.randint(-5, 5), random.randint(1, 5))

# ---------------------------------------

def draw():
  screen.clear()
  spacecraft.draw()
  rock.draw()

  # Check to see if the game is over
  if gameOver:
    # If the game is over, then print a series of red rectangles
    # with a text message.
    for i in range(20,-5,-5):
      screen.draw.filled_rect(Rect((centre_x-(100+i), centre_y-(30+i)), (200+(i*2), 80+(i*2))), (200-(i*8), 0, 0))
    screen.draw.text("GAME OVER!", center=(centre_x, centre_y))
    screen.draw.text("(spacebar to restart)", center=(centre_x, centre_y+20))

# ---------------------------------------

def updateSpacecraft():
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

# ---------------------------------------

def updateRock():
  global rock
  global rock_vx
  global rock_vy
  # Check if the rock has gone off the screen.  If it has, then
  # reset its starting position and initial velocity.
  if rock.right < 0 or rock.left > WIDTH or rock.top > HEIGHT:
    (rock.x, rock.y) = startingPosition()
    (rock_vx, rock_vy) = startingVelocity()
    rock.image = 'rock'  # If it has been destroyed, make it a normal rock again

  # Move the x position by the corresponding velocity component
  rock.x += rock_vx

  # Move the y position by the corresponding velocity component
  rock.y += rock_vy 

# ---------------------------------------

def update():
  global gameOver

  # If the game is not over, move the spacecraft and rock
  if not gameOver:
    updateSpacecraft()
    updateRock()
  else:
    # If the game is over, test to see if the spacebar has been pressed.
    # If it has been pressed, reset the positions of the spracecraft and
    # rock and restart the game.
    if keyboard.space:
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
  
