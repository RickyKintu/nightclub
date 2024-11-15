import pygame
import sys

# Initialize Pygame
pygame.init()

# Load the sprite sheet from the specified path
sprite_sheet = pygame.image.load('./assets/32x32/Char_001.png')

# Frame size and layout information
frame_width = 32   # Width of each frame
frame_height = 40  # Height adjusted to capture the entire character including legs
frames_per_row = 4  # Number of frames in the row

# Adjust X and Y positions to skip padding
initial_x_offset = 8  # Skip 8 pixels from the left to avoid initial padding
second_row_y = 152    # Adjust y-position based on the required row (e.g., first row = 8, second row = 57, etc.)

# Extract frames from the specified row, accounting for 8px margin between frames
frames = []
for col in range(frames_per_row):
    x = initial_x_offset + col * (frame_width + 16)  # Add 16 pixels (8px padding on both sides) between frames
    y = second_row_y
    frame = sprite_sheet.subsurface((x, y, frame_width, frame_height)).copy()
    frames.append(frame)

# Set up display for animation
screen_width = frame_width * 2
screen_height = frame_height * 2
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill((255, 255, 255))

# Animation variables
current_frame = 0
frame_duration = 200  # Duration for each frame in milliseconds
last_update = pygame.time.get_ticks()

# Main loop to display animation
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the frame based on time
    now = pygame.time.get_ticks()
    if now - last_update > frame_duration:
        current_frame = (current_frame + 1) % len(frames)  # Cycle through frames
        last_update = now

    # Clear screen
    screen.fill((255, 255, 255))
    # Draw the current frame in the center of the screen without a border
    frame = pygame.transform.scale(frames[current_frame], (frame_width * 2, frame_height * 2))  # Scale for visibility
    screen.blit(frame, ((screen_width - frame_width * 2) // 2, (screen_height - frame_height * 2) // 2))
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.delay(100)

pygame.quit()
sys.exit()
