# main.py

import pygame
import sys
import time
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK
from draw_elements import draw_dance_floor, draw_speakers_and_table, draw_spotlights
from components.menu import draw_vertical_menu
from components.stats import draw_stats
from components.guest import Guest
from components.walkway import Walkway

# Initialize the walkway with a starting position and desired lengths
walkway = Walkway(start_x=700, start_y=SCREEN_HEIGHT - 50, length=300, turn_length=200)

# Define dance floor dimensions
DANCE_FLOOR_TOP_LEFT = (300, 150)  # Exact upper-left corner of dance floor
TILE_SIZE = 40                     # Exact tile size
DANCE_FLOOR_ROWS = 10
DANCE_FLOOR_COLS = 10

# Define function to get a random position on the dance floor
def get_random_dance_floor_position():
    col = random.randint(0, DANCE_FLOOR_COLS - 1)
    row = random.randint(0, DANCE_FLOOR_ROWS - 1)
    x = DANCE_FLOOR_TOP_LEFT[0] + col * TILE_SIZE + TILE_SIZE // 2
    y = DANCE_FLOOR_TOP_LEFT[1] + row * TILE_SIZE + TILE_SIZE // 2
    return x, y

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Nattklubbsspel - Converging Waves Effect")

# Variables for controlling the waves
last_update_time = time.time() * 1000
wave_interval = 300
wave_step = 0
wave_expanding = True

# Variables for controlling the sound waves
wave_timer = 0
light_timer = 0

# Initialize stats
money = 1000
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

    # Check if the guest count has increased
    if guests > previous_guest_count:
        # Generate a new random position on the dance floor for each guest
        random_dance_floor_position = get_random_dance_floor_position()
        waypoints = [
            (spawn_x, spawn_y),                         # Starting point
            (spawn_x, spawn_y - 300),                   # Move up to the turn
            (spawn_x - 200, spawn_y - 300),             # Turn left along the horizontal section
            random_dance_floor_position                 # Random tile on the dance floor
        ]
        new_guest = Guest(start_x=spawn_x, start_y=spawn_y, waypoints=waypoints)
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

    # Update and draw guests
    for guest in guest_instances:
        guest.move()
        guest.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
