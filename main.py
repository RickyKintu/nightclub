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
from components.modal import Modal
from components.shop_catalog import ShopCatalog
from components.bouncer import Bouncer

# Initialize the walkway with a starting position and desired lengths
walkway = Walkway(start_x=700, start_y=SCREEN_HEIGHT - 50, length=300, turn_length=200)

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Nattklubbsspel - Converging Waves Effect")

# Fullscreen toggle variables
is_fullscreen = False

# Load multiple character sprite sheets
character_sprites = [
    pygame.image.load(f'./assets/32x32/Char_00{i}.png').convert_alpha() for i in range(1, 6)
]

bouncer_sprite = pygame.image.load('./assets/32x32/Char_006.png').convert_alpha()

# Resize dynamically for chat bubbles
guest_width = 20
bubble_width = guest_width
bubble_height = guest_width

bubble_images = {
    "thirsty": pygame.transform.scale(
        pygame.image.load('./assets/chatbubbles/beer.png').convert_alpha(),
        (bubble_width, bubble_height)
    ),
    "toilet": pygame.transform.scale(
        pygame.image.load('./assets/chatbubbles/toilet.png').convert_alpha(),
        (bubble_width, bubble_height)
    ),
    "hungry": pygame.transform.scale(
        pygame.image.load('./assets/chatbubbles/hungry.png').convert_alpha(),
        (bubble_width, bubble_height)
    ),
}

# Variables for controlling the waves
last_update_time = time.time() * 1000
wave_interval = 300
wave_step = 0
wave_expanding = True

# Variables for controlling the sound waves
wave_timer = 0
light_timer = 0

# Initialize stats
money = [2000]  # Use a list to pass money by reference
guests = 1  # Start with 1 guest
capacity = 20
security = 0

# Guest management
guest_instances = []
previous_guest_count = 0  # Ensure guest is added on startup

# Bouncer management
bouncers = []  # List to hold all Bouncer instances

# Use the arrow's position as the spawn point for guests
spawn_x, spawn_y = walkway.stanchions[0][0] + 25, walkway.stanchions[0][1] + 20

# Modal instance
modal = None

# Initialize the shop catalog
categories = {
    "Security": [("Bouncer", 500), ("Cameras", 300), ("Metal Detector", 700)],
    "Lights": [("LED Strips", 200), ("Spotlights", 400), ("Disco Ball", 600)],
    "DJ": [("Basic DJ Table", 1000), ("Advanced DJ Kit", 2000), ("Speakers", 1500)],
    "Bars": [("Small Bar", 800), ("Medium Bar", 1200), ("Premium Bar", 2000)],
}

shop_catalog = ShopCatalog(screen, categories, money, bouncer_sprite, walkway, bouncers)

# Shop state
shop_open = False

# Main game loop
running = True
while running:
    screen.fill(BLACK)  # Clear the screen at the start of each frame

    # Draw the vertical menu and get button rects
    button_rects = draw_vertical_menu(screen)

    # Event handling
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle shop-specific events if the shop is open
        if shop_open:
            action = shop_catalog.handle_event(event)
            if action == "close":  # Close the shop if needed
                shop_open = False
        else:
            # Game events
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                if modal:
                    # Check if the "X" button in the modal is clicked
                    x_button_rect = modal.draw()
                    if x_button_rect and x_button_rect.collidepoint(mouse_pos):
                        modal = None  # Close the modal
                else:
                    # Check if any guest is clicked
                    for guest in guest_instances:
                        if guest.is_clicked(mouse_pos):
                            modal = Modal(screen, guest)  # Open a modal for the clicked guest
                            break

            # Handle menu buttons
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rects["Shop"].collidepoint(mouse_pos):
                    shop_open = True
                if button_rects["Add guest"].collidepoint(mouse_pos):
                    guests += 1

            # Handle fullscreen toggle
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                is_fullscreen = not is_fullscreen
                if is_fullscreen:
                    info = pygame.display.Info()
                    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Update game elements only when the shop is closed
    if not shop_open:
        # Update the wave every few frames
        current_time = time.time() * 1000
        wave_timer += 0.1
        light_timer += 1

        if current_time - last_update_time >= wave_interval:
            if wave_expanding:
                wave_step += 1
                if wave_step >= 10:
                    wave_expanding = False
            else:
                wave_step -= 1
                if wave_step <= 1:
                    wave_expanding = True
            last_update_time = current_time

        # Check if the guest count has increased
        if guests > previous_guest_count:
            random_dance_floor_position = get_random_dance_floor_tile()
            waypoints = [
                (spawn_x, spawn_y),
                (spawn_x, spawn_y - 300),
                (spawn_x - 200, spawn_y - 300),
                random_dance_floor_position,
            ]
            random_sprite_sheet = random.choice(character_sprites)
            new_guest = Guest(
                start_x=spawn_x,
                start_y=spawn_y,
                waypoints=waypoints,
                sprite_sheet=random_sprite_sheet,
                get_random_dance_floor_tile=get_random_dance_floor_tile,
            )
            guest_instances.append(new_guest)
            previous_guest_count = guests


        security = str(len(bouncers))
        # Draw game elements
        draw_stats(screen, money[0], guests, capacity, security)
        draw_dance_floor(screen, wave_step)
        draw_speakers_and_table(screen, wave_timer)
        draw_spotlights(screen, light_timer)
        walkway.draw(screen)

        # Draw all Bouncers
        for bouncer in bouncers:
            bouncer.draw(screen)

        # Move and draw guests
        for guest in guest_instances:
            guest.update_need(bubble_images)
            guest.move()
            guest.draw(screen)

        # Draw the modal if it exists
        if modal:
            modal.draw()

    # Draw the shop catalog if it's open
    if shop_open:
        shop_catalog.draw()

    pygame.display.flip()

pygame.quit()
sys.exit()
