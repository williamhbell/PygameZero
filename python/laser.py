import random

# Set the size of the window
WIDTH = 600
HEIGHT = 500

# Create the actors
spacecraft = Actor('spacecraft')    # The spacecraft actor
rock = Actor('rock') # Rock actor with the same image

# Create the laser rect
laser = Rect((0,-HEIGHT*4), (2, 1000))  # Created, but not within the screen area.

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
  return (random.randint(0, WIDTH), 0)

# ---------------------------------------

def startingVelocity():
  return (random.randint(-5, 5), random.randint(1, 5))

# ---------------------------------------

def initialRockPosition():
  global rock
  global rock_vx
  global rock_vy
  global rmRock
  rock.image = 'rock' # In case it has been destroyed
  rock.pos = 0, HEIGHT*2 # Off the screen
  rock_vx = 0
  rock_vy = 0
  (rock.x, rock.y) = startingPosition()
  (rock_vx, rock_vy) = startingVelocity()
  rock.image = 'rock'
  rmRock = False

# ---------------------------------------

def initialPositions():
  global spacecraft
  global score
  spacecraft.image = 'spacecraft' # In case it has been destroyed
  # Initial position and velocity
  spacecraft.pos = centre_x, centre_y # Inital position of the spacecraft
  initialRockPosition()
  score = 0

# ---------------------------------------

# Starting settings for the game
initialPositions()

# ---------------------------------------

def laserFiringComplete():
  global laserFiring
  laserFiring = False
  clock.schedule(laserChargingComplete, 1.0)

# ---------------------------------------

def laserChargingComplete():
  global laserCharged
  laserCharged = True

# ---------------------------------------

def removeRock():
  global rmRock
  rmRock = True

# ---------------------------------------

def draw():
  global laser
  screen.clear()
  spacecraft.draw()
  rock.draw()

  screen.draw.text("Score : "+str(score), center=(centre_x-100, HEIGHT-10.))
  screen.draw.text("Top Score : "+str(topScore), center=(centre_x+100, HEIGHT-10.))

  if laserFiring:
    screen.draw.filled_rect(laser,(0,255,0))

  if gameOver:
    for i in range(20,-5,-5):
      screen.draw.filled_rect(Rect((centre_x-(100+i), centre_y-(30+i)), (200+(i*2), 80+(i*2))), (200-(i*8), 0, 0))
    screen.draw.text("GAME OVER!", center=(centre_x, centre_y))
    screen.draw.text("(n to restart)", center=(centre_x, centre_y+20))

# ---------------------------------------

def updateSpacecraft():
  global laserFiring
  global laserCharged
  global laser
  if keyboard.left and spacecraft.left > 2:
    spacecraft.x -= 2
  if keyboard.right and spacecraft.right < WIDTH+2:
    spacecraft.x += 2
  if keyboard.down and spacecraft.bottom < HEIGHT+2:
    spacecraft.y += 2
  if keyboard.up and spacecraft.top > 2:
    spacecraft.y -= 2

  if keyboard.space and laserCharged:
    laserCharged = False
    laserFiring = True
    clock.schedule(laserFiringComplete, 0.3)

  if laserFiring:
    laser = Rect((spacecraft.x-2,0),(4,spacecraft.top))

# ---------------------------------------

def updateRock():
  global rock
  if rock.right < 0 or rock.left > WIDTH or rock.bottom > HEIGHT or rmRock:
    initialRockPosition()
  rock.x += rock_vx
  rock.y += rock_vy

# ---------------------------------------

def update():
  global gameOver
  global score
  global topScore

  if not gameOver:
    updateSpacecraft()
    updateRock()
  else:
    if keyboard.n:
      initialPositions()
      gameOver = False

  collision = spacecraft.colliderect(rock)
  if collision:
    rock.image = 'rock_destroyed'
    spacecraft.image = 'spacecraft_destroyed'
    gameOver = True
  
  rockLaser = rock.colliderect(laser)
  if rockLaser and laserFiring and rock.image != 'rock_destroyed':
    rock.image = 'rock_destroyed'
    score = score + 1
    if score > topScore:
      topScore = score
    clock.schedule(removeRock, 0.2)
