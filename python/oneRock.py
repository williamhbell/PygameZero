import random

# Set the size of the window
WIDTH = 600
HEIGHT = 500

# Create the actors
spacecraft = Actor('spacecraft')    # The spacecraft actor
rock = Actor('rock') # Rock actor with the same image

# The centre of the screen
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
  rock_vx = 0
  rock_vy = 0

# ---------------------------------------

# Starting settings for the game
gameOver = False
initialPositions()

# ---------------------------------------

def startingPosition():
  return (random.randint(0, WIDTH), 0)

# ---------------------------------------

def startingVelocity():
  return (random.randint(-5, 5), random.randint(1, 5))

# ---------------------------------------

def draw():
  screen.clear()
  spacecraft.draw()
  rock.draw()

  if gameOver:
    for i in range(20,-5,-5):
      screen.draw.filled_rect(Rect((centre_x-(100+i), centre_y-(30+i)), (200+(i*2), 80+(i*2))), (200-(i*8), 0, 0))
    screen.draw.text("GAME OVER!", center=(centre_x, centre_y))
    screen.draw.text("(spacebar to restart)", center=(centre_x, centre_y+20))

# ---------------------------------------

def updateSpacecraft():
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
  if rock.right < 0 or rock.left > WIDTH or rock.top > HEIGHT:
    (rock.x, rock.y) = startingPosition()
    (rock_vx, rock_vy) = startingVelocity()
    rock.image = 'rock'
  rock.x += rock_vx
  rock.y += rock_vy

# ---------------------------------------

def update():
  global gameOver
  if not gameOver:
    updateSpacecraft()
    updateRock()
  else:
    if keyboard.space:
      initialPositions()
      gameOver = False

  collision = spacecraft.colliderect(rock)
  if collision:
    rock.image = 'rock_destroyed'
    spacecraft.image = 'spacecraft_destroyed'
    gameOver = True
  
