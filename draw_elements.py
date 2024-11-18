# draw_elements.py

import pygame
import random
from settings import  SCREEN_WIDTH, SCREEN_HEIGHT,GRAY, SPEAKER_COLOR, TABLE_COLOR, DOORWAY_X, DOORWAY_Y, DOORWAY_LIGHT_COLOR
from components.spotlight import Spotlight



# Define neon colors for the wave effect
NEON_COLORS = [
    (255, 255, 0),  # Yellow
    (0, 102, 255),  # Blue
    (255, 0, 255),  # Purple
    (0, 255, 180),  # Turquoise
    (255, 102, 0)   # Orange
]

def get_random_dance_floor_tile():
    # Dance floor parameters
    top_left = (300, 150)
    top_right = (500, 150)
    bottom_left = (250, 350)
    rows = 10
    cols = 10

    # Select a random row and column
    row = random.randint(0, rows - 1)
    col = random.randint(0, cols - 1)

    # Calculate the center position of the selected tile
    start_x = top_left[0] + col * (top_right[0] - top_left[0]) // cols + row * (bottom_left[0] - top_left[0]) // rows
    start_y = top_left[1] + row * (bottom_left[1] - top_left[1]) // rows
    tile_width = (top_right[0] - top_left[0]) // cols
    tile_height = (bottom_left[1] - top_left[1]) // rows

    # Return the center of the tile
    return (start_x + tile_width // 2, start_y + tile_height // 2)

def draw_dance_floor(screen, wave_step):
    top_left = (300, 150)
    top_right = (500, 150)
    bottom_right = (450, 350)
    bottom_left = (250, 350)

    rows = 10
    cols = 10
    margin = 2  # Margin between tiles

    # Draw each tile based on distance from two corners
    for row in range(rows):
        for col in range(cols):
            distance_from_bottom_left = row + col
            distance_from_top_right = (rows - 1 - row) + (cols - 1 - col)

            if distance_from_bottom_left <= wave_step:
                color_index = distance_from_bottom_left % len(NEON_COLORS)
                tile_color = NEON_COLORS[color_index]
            elif distance_from_top_right <= wave_step:
                color_index = distance_from_top_right % len(NEON_COLORS)
                tile_color = NEON_COLORS[color_index]
            else:
                tile_color = GRAY

            start_x = top_left[0] + col * (top_right[0] - top_left[0]) // cols + row * (bottom_left[0] - top_left[0]) // rows
            start_y = top_left[1] + row * (bottom_left[1] - top_left[1]) // rows
            tile_width = (top_right[0] - top_left[0]) // cols - margin
            tile_height = (bottom_left[1] - top_left[1]) // rows - margin

            pygame.draw.rect(screen, tile_color, pygame.Rect(start_x, start_y, tile_width, tile_height))


def draw_speakers_and_table(screen, wave_timer):
    # Positions for speakers and table
    speaker_y_position = 50  # Y position for speakers
    table_y_position = speaker_y_position + 100  # Position the table below the speakers

    # Draw the DJ table first so it appears behind the speakers
    pygame.draw.rect(screen, TABLE_COLOR, pygame.Rect(350, table_y_position - 50, 100, 20))

    # Define speaker boxes
    left_speaker_rect = pygame.Rect(330, speaker_y_position, 40, 80)
    right_speaker_rect = pygame.Rect(430, speaker_y_position, 40, 80)

    # Draw the speaker boxes on top of the table
    pygame.draw.rect(screen, SPEAKER_COLOR, left_speaker_rect)
    pygame.draw.rect(screen, SPEAKER_COLOR, right_speaker_rect)

    # Draw speaker cones with an inner circle for depth
    def draw_speaker_cone(centerx, centery):
        # Outer speaker cone
        pygame.draw.circle(screen, GRAY, (centerx, centery), 15)
        # Inner dark circle for depth
        pygame.draw.circle(screen, (50, 50, 50), (centerx, centery), 8)

        # Draw sound waves radiating from the center of each speaker
        max_radius = 40  # Maximum radius for the sound waves
        for i in range(3):  # Number of waves
            # Calculate expanding radius based on wave_timer
            radius = (wave_timer + i * 10) % max_radius
            transparency = max(0, 255 - (radius * 6))  # Fade out as radius increases
            wave_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.circle(wave_surface, (200, 200, 200, transparency), (centerx, centery), radius, 2)
            screen.blit(wave_surface, (0, 0))

    # Left Speaker
    draw_speaker_cone(left_speaker_rect.centerx, left_speaker_rect.centery)

    # Right Speaker
    draw_speaker_cone(right_speaker_rect.centerx, right_speaker_rect.centery)


# Function to draw multiple spotlights
def draw_spotlights(screen, light_timer, level=1):
    # Define colors and positions for spotlights
    disco_colors = [
        (255, 0, 0),  # Red
        (0, 255, 0),  # Green
        (0, 0, 255),  # Blue
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Purple
        (0, 255, 255)  # Cyan
    ]

    # Cycle color based on timer
    color = disco_colors[int((light_timer / 10) % len(disco_colors))]

    # Create spotlights with a rotated stick fixture
    left_spotlight = Spotlight(SCREEN_WIDTH // 4, 30, color, 0, num_bulbs=1, rotation_angle=60)
    right_spotlight = Spotlight(3 * SCREEN_WIDTH // 4, 30, color, -50, num_bulbs=1, rotation_angle=-60)

    # Draw spotlights
    left_spotlight.draw(screen)
    right_spotlight.draw(screen)


