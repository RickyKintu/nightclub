import pygame

# Define colors
GOLD = (255, 215, 0)
HOVER_COLOR = (255, 223, 120)
BACKGROUND_COLOR = (30, 30, 30)
BUTTON_SHADOW_COLOR = (20, 20, 20)
TEXT_COLOR = (0, 0, 0)

# Menu items with optional icons
menu_items = [
    ("Shop", "assets/icons/upgrade.png"),
    ("Light", "assets/icons/upgrade.png"),
    ("Security", "assets/icons/upgrade.png"),
    ("Add guest", "assets/icons/upgrade.png"),
]

def load_icons():
    """Load menu item icons."""
    icons = {}
    for item, icon_path in menu_items:
        icons[item] = pygame.image.load(icon_path).convert_alpha()
    return icons

def draw_vertical_menu(screen, dropdown_open):
    """Draws the vertical menu with the dropdown for the Shop button."""
    font = pygame.font.Font(None, 24)
    bar_width = 140
    bar_height = 60
    spacing = 20
    start_x = 20
    start_y = 40
    shadow_offset = 5  # Offset for shadow effect

    menu_items = [
        {"label": "Add guest", "action": "add_guest"},
        {"label": "Shop", "action": "shop"},
    ]

    dropdown_items = ["DJ", "Security", "Lights", "Bars"]

    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rects = {}

    # Draw each menu item
    for i, item in enumerate(menu_items):
        x = start_x
        y = start_y + i * (bar_height + spacing)

        # Check hover
        is_hovered = x <= mouse_x <= x + bar_width and y <= mouse_y <= y + bar_height
        button_color = HOVER_COLOR if is_hovered else GOLD

        # Draw shadow
        pygame.draw.rect(
            screen,
            BUTTON_SHADOW_COLOR,
            (x + shadow_offset, y + shadow_offset, bar_width, bar_height),
            border_radius=15,
        )

        # Draw button
        pygame.draw.rect(screen, button_color, (x, y, bar_width, bar_height), border_radius=15)

        # Draw text
        text_surface = font.render(item["label"], True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(x + bar_width // 2, y + bar_height // 2))
        screen.blit(text_surface, text_rect)

        # Save button rect
        button_rects[item["label"]] = pygame.Rect(x, y, bar_width, bar_height)

        # If dropdown is open, draw dropdown items
        if item["label"] == "Shop" and dropdown_open:
            dropdown_start_x = x  # Align dropdown with the Shop button
            dropdown_start_y = y + bar_height + 5 # Start directly below the Shop button
            dropdown_width = bar_width  # Match the width of the Shop button
            dropdown_height = 40

            for j, dropdown_item in enumerate(dropdown_items):
                dropdown_y = dropdown_start_y + j * (dropdown_height + 5)

                # Check hover
                is_hovered = (
                    dropdown_start_x <= mouse_x <= dropdown_start_x + dropdown_width
                    and dropdown_y <= mouse_y <= dropdown_y + dropdown_height
                )
                dropdown_color = HOVER_COLOR if is_hovered else (200, 200, 200)

                # Draw dropdown item
                pygame.draw.rect(
                    screen,
                    dropdown_color,
                    (dropdown_start_x, dropdown_y, dropdown_width, dropdown_height),
                    border_radius=10,
                )

                # Draw text
                dropdown_text_surface = font.render(dropdown_item, True, TEXT_COLOR)
                dropdown_text_rect = dropdown_text_surface.get_rect(
                    center=(dropdown_start_x + dropdown_width // 2, dropdown_y + dropdown_height // 2)
                )
                screen.blit(dropdown_text_surface, dropdown_text_rect)

                # Save dropdown rect
                button_rects[dropdown_item] = pygame.Rect(
                    dropdown_start_x, dropdown_y, dropdown_width, dropdown_height
                )

    return button_rects
