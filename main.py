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
from progress_manager import load_progress, save_progress, reset_progress

# Ladda spelarens framsteg
player_progress = load_progress()

session_duration = 25 * 60  # 25 minuter i sekunder
session_start_time = time.time()  # Starttid för sessionen


# Initialize the walkway with a starting position and desired lengths
walkway = Walkway(start_x=700, start_y=SCREEN_HEIGHT - 50, length=300, turn_length=200)

# Define bouncer blocking position (e.g., near the entrance)
BLOCKING_POSITION = (walkway.stanchions[-1][0] - 30, walkway.stanchions[-1][1] - 40)

# Define the queue starting position near the bouncer
QUEUE_START_X = BLOCKING_POSITION[0]
QUEUE_START_Y = BLOCKING_POSITION[1] + 50  # Adjusted below the bouncer for queuing guests

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

selected_guest = None  # Track the currently selected guest
modal = None  # Track the modal instance

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

dropdown_open = False  # Track whether the dropdown menu is open


# Main game loop
running = True
while running:
    screen.fill(BLACK)  # Clear the screen at the start of each frame


    
    # Draw the vertical menu and get button rects
    button_rects = draw_vertical_menu(screen, dropdown_open)

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
                        selected_guest.selected = False  # Allow movement for deselected guest
                        modal = None  # Close the modal
                        selected_guest = None  # Deselect the guest

                else:
                    # Check if any guest is clicked
                    for guest in guest_instances:
                        if guest.selected:
                            print(f"Selected Guest at ({guest.x}, {guest.y}) is stationary.")
                        else:
                            print(f"Moving Guest at ({guest.x}, {guest.y})")
                        if guest.is_clicked(mouse_pos):
                            if selected_guest:  # Deselect the previously selected guest
                                selected_guest.selected = False
                            selected_guest = guest  # Set the clicked guest as selected
                            selected_guest.selected = True  # Explicitly mark this guest as selected
                            modal = Modal(screen, guest)  # Modal will now slide below the guest
                            break

                    if dropdown_open:
                        for category in categories.keys():  # Loop through dropdown items
                            if button_rects.get(category) and button_rects[category].collidepoint(mouse_pos):
                                print(f"Selected {category}")
                                shop_catalog.open_category(category)  # Open the shop catalog for the selected category
                                shop_open = True  # Open shop
                                dropdown_open = False  # Close dropdown
                                break
                        else:
                            dropdown_open = False  # Close dropdown if clicked outside

            # Handle menu buttons
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rects["Shop"].collidepoint(mouse_pos):
                    dropdown_open = not dropdown_open  # Toggle the dropdown menu
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

        # Update game stats
        security = str(len(bouncers))
        draw_stats(screen, money[0], guests, capacity, security)

        # Draw game elements
        draw_dance_floor(screen, wave_step)
        draw_speakers_and_table(screen, wave_timer)
        draw_spotlights(screen, light_timer)
        walkway.draw(screen)

        # Bouncer and capacity handling
        if guests > capacity:
            if bouncers:
                bouncers[0].target_x, bouncers[0].target_y = BLOCKING_POSITION
                bouncers[0].move_to_target()

            # Line guests vertically in front of the bouncer
            for i, guest in enumerate([g for g in guest_instances if g.current_waypoint == 0]):
                guest.target_location = (QUEUE_START_X, QUEUE_START_Y + i * 40)  # Offset each guest below the last
        else:
            for guest in guest_instances:
                guest.pause_timer = 0

        # Draw all bouncers
        for bouncer in bouncers:
            bouncer.draw(screen)

        # Move and draw guests
        for guest in guest_instances:
            guest.update_need(bubble_images)
            guest.move()
            is_selected = (guest == selected_guest)  # Check if this guest is selected
            is_faded = not is_selected and selected_guest is not None  # Fade out unselected guests
            guest.draw(screen, is_selected=is_selected, is_faded=is_faded)

        # Draw the modal if it exists
        if modal:
            modal.draw()

    # Draw the shop catalog if it's open
    if shop_open:
        shop_catalog.draw()

    pygame.display.flip()

pygame.quit()
sys.exit()
