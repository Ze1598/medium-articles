import pygame
from random import randint, choice

# RGB colours
BLACK = (0, 0,0)
WHITE = (255, 255, 255)
GREEN = (44, 205, 23)
RED = (216, 10, 0)
BLUE = (27, 64, 255)
PURPLE = (121, 0, 234)
YELLOW = (236, 197, 0)
SILVER = (217, 217, 220)
COLOUR_OPTIONS = (RED, GREEN, BLUE, PURPLE, YELLOW, SILVER)
# Flag to run main loop
done = False
# Number of gems to draw initially
num_gems = 285

# Set window size
size = (900, 600)
screen = pygame.display.set_mode(size)
# Used to control frame rate
clock = pygame.time.Clock()
#Start the engine
pygame.init()

# Each gem is a 6-sided polygon with 6 (x,y) cooridnates
def generate_gem(first_gen=False):
    # First generation places gems all over the screen
    if first_gen == True:
        top_left = [randint(0, size[0]), randint(0, size[1])]
    # Other generations place gems at the top of the screen
    else:
        # top_left = [randint(0,size[0]), randint(-50,100)]
        top_left = [randint(0, size[0]), randint(-50, 0)]
        
    top_right = [top_left[0] + 16, top_left[1]]
    top_middle = [(top_left[0] + top_right[0]) // 2, (top_left[1] + top_right[1]) // 2 - 10]
    
    bottom_left = [top_left[0], top_left[1] + 20]
    bottom_right = [top_right[0], top_right[1] + 20]
    bottom_middle = [top_middle[0], top_middle[1] + 40]
    
    # Randomise colour
    colour = choice(COLOUR_OPTIONS)
    
    # The gem is 6-sided, but the 7th list element is the gem colour
    return [top_left, top_middle, top_right, bottom_right, bottom_middle, bottom_left, colour]

# Running list of gems, initially populated with the first set of gems
gems_list = [generate_gem(first_gen=True) for gem in range(num_gems)]

# Main loop - each iteration is a frame
while not done:
    
    # Check for new user events and finish the animation if the user quits
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Fill screen black on every frame
    screen.fill(BLACK)

    # Draw each gem
    for i in range(len(gems_list)):
        gem_coordinates = gems_list[i][:6]
        gem_colour = gems_list[i][6]
        
        # Last parameter as 0 fills the polygon with the given colour
        pygame.draw.polygon(screen, gem_colour, gem_coordinates, 0)
        
        # Increment Y coordinate of each vertex to move gem down
        gems_list[i] = [
            [gem_coordinates[vertex][0], gem_coordinates[vertex][1] + 4] 
            for vertex in range(6)
        ] + [gem_colour]
            
        # Replace gems going out of bounds by new ones placed at the top of the screen
        gem_middle_bottom_y = gems_list[i][4][1]
        if gem_middle_bottom_y > size[1]:
            gems_list[i] = generate_gem()

    # Wait until everything is drawn to display on screen
    pygame.display.flip()
    # FPS count
    clock.tick(60)

#Quit the program properly
pygame.quit()