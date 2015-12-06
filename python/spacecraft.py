# Set the size of the window
WIDTH = 600
HEIGHT = 500

# Create the actors
spacecraft = Actor('spacecraft')    # The spacecraft actor
spacecraft.pos = WIDTH/2, HEIGHT/2  # The initial position of the spacecraft

# ---------------------------------------
# The draw function
def draw():
  screen.clear()
  spacecraft.draw()

# ---------------------------------------
# The update function
def update():

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
  
