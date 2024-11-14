# components/menu.py

import pygame

# Define gold color for the menu
GOLD = (255, 215, 0)
HOVER_COLOR = (255, 223, 120)  # Lighter shade of gold for hover effect

# Define menu items
menu_items = ["Upgrade", "DJ", "Light", "Security", "Add guest"]

def draw_vertical_menu(screen):
    font = pygame.font.SysFont("Arial", 24)  # Choose a font and size
    bar_width = 120
    bar_height = 60
    spacing = 20
    start_y = 40  # Starting y-coordinate for the menu

    # Get the mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    add_guest_button_rect = None  # Initialize a variable to store "Add guest" button rect

    for i, item in enumerate(menu_items):
        # Calculate position for each menu item
        x = 20  # Fixed x-coordinate for left alignment
        y = start_y + i * (bar_height + spacing)

        # Check if the mouse is over this menu item
        is_hovered = x <= mouse_x <= x + bar_width and y <= mouse_y <= y + bar_height

        # Choose color based on hover state
        color = HOVER_COLOR if is_hovered else GOLD

        # Draw the rectangle
        pygame.draw.rect(screen, color, (x, y, bar_width, bar_height))

        # Render text
        text_surface = font.render(item, True, (0, 0, 0))  # Black text for contrast
        text_rect = text_surface.get_rect(center=(x + bar_width // 2, y + bar_height // 2))
        screen.blit(text_surface, text_rect)

        # Store the "Add guest" button rect for click detection
        if item == "Add guest":
            add_guest_button_rect = pygame.Rect(x, y, bar_width, bar_height)

    return add_guest_button_rect
