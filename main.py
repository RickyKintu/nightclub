# main.py

import pygame
import sys
import time
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK
from draw_elements import draw_dance_floor, draw_speakers_and_table, draw_spotlights, get_random_dance_floor_tile
from components.menu import draw_vertical_menu
from components.stats import draw_stats
from components.guest import Guest
from components.walkway import Walkway

# Initialize the walkway with a starting position and desired lengths
walkway = Walkway(start_x=700, start_y=SCREEN_HEIGHT - 50, length=300, turn_length=200)

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Nattklubbsspel - Converging Waves Effect")

# Load multiple character sprite sheets
character_sprites = [
    pygame.image.load(f'./assets/32x32/Char_00{i}.png').convert_alpha() for i in range(1, 7)
]



# Variables for controlling the waves
last_update_time = time.time() * 1000
wave_interval = 300
wave_step = 0
wave_expanding = True

# Variables for controlling the sound waves
wave_timer = 0
light_timer = 0

# Initialize stats
money = 2000
guests = 1  # Start with 1 guest
capacity = 20
security = 0

# Guest management
guest_instances = []
previous_guest_count = 0  # Ensure guest is added on startup

# Use the arrow's position as the spawn point for guests
spawn_x, spawn_y = walkway.stanchions[0][0] + 25, walkway.stanchions[0][1] + 20

# Main game loop
running = True
while running:
    screen.fill(BLACK)  # Clear the screen at the start of each frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            # Check if "Add guest" button was clicked
            if add_guest_button_rect and add_guest_button_rect.collidepoint(event.pos):
                guests += 1  # Add a new guest

     # Draw the vertical menu on the left and get the "Add guest" button rect
    add_guest_button_rect = draw_vertical_menu(screen)

    # Update the wave every few frames
    current_time = time.time() * 1000
    wave_timer += 0.1
    light_timer += 1

    DANCE_FLOOR_BOUNDS = (300, 150, 400, 400)  # Adjust these values to match your dance floor area


    # Check if the guest count has increased
    if guests > previous_guest_count:
        # Generate a new random position on the dance floor for each guest
        random_dance_floor_position = get_random_dance_floor_tile()
        waypoints = [
            (spawn_x, spawn_y),                         # Starting point
            (spawn_x, spawn_y - 300),                   # Move up to the turn
            (spawn_x - 200, spawn_y - 300),             # Turn left along the horizontal section
            random_dance_floor_position                 # Random tile on the dance floor
        ]

        # Choose a random character sprite sheet for the new guest
        random_sprite_sheet = random.choice(character_sprites)

        new_guest = Guest(start_x=spawn_x, start_y=spawn_y, waypoints=waypoints, sprite_sheet=random_sprite_sheet,    get_random_dance_floor_tile=get_random_dance_floor_tile
)
        guest_instances.append(new_guest)
        previous_guest_count = guests

    if current_time - last_update_time >= wave_interval:
        # Update the wave step and check for expansion/contraction
        if wave_expanding:
            wave_step += 1
            if wave_step >= 10:
                wave_expanding = False
        else:
            wave_step -= 1
            if wave_step <= 1:
                wave_expanding = True
        last_update_time = current_time

    # Draw the vertical menu on the left
    draw_vertical_menu(screen)

    # Draw stats on the right side
    draw_stats(screen, money, guests, capacity, security)

    # Draw the dance floor with the current wave step
    draw_dance_floor(screen, wave_step)
    draw_speakers_and_table(screen, wave_timer)
    draw_spotlights(screen, light_timer)
    walkway.draw(screen)

   
    # Debugging visuals and guest movement
    for guest in guest_instances:
        # Move and draw each guest
        guest.move()
        guest.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()
