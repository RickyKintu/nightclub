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

def draw_vertical_menu(screen):
    font = pygame.font.SysFont("Arial", 20, bold=True)  # Modern font with bold styling
    bar_width = 140
    bar_height = 60
    spacing = 20
    start_y = 40
    shadow_offset = 5  # Offset for shadow effect

    # Load icons
    icons = load_icons()

    # Get the mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    button_rects = {}

    for i, (item, _) in enumerate(menu_items):
        # Calculate button position
        x = 20
        y = start_y + i * (bar_height + spacing)

        # Check hover state
        is_hovered = x <= mouse_x <= x + bar_width and y <= mouse_y <= y + bar_height
        button_color = HOVER_COLOR if is_hovered else GOLD

        # Draw shadow
        pygame.draw.rect(
            screen,
            BUTTON_SHADOW_COLOR,
            (x + shadow_offset, y + shadow_offset, bar_width, bar_height),
            border_radius=15,
        )

        # Draw button with rounded corners
        pygame.draw.rect(
            screen,
            button_color,
            (x, y, bar_width, bar_height),
            border_radius=15,
        )

        # Render icon if available
        icon = icons.get(item)
        if icon:
            icon = pygame.transform.scale(icon, (30, 30))  # Scale icon to fit
            screen.blit(icon, (x + 10, y + (bar_height - 30) // 2))

        # Render text
        text_surface = font.render(item, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(
            center=(x + bar_width // 2 + 20, y + bar_height // 2)
        )  # Offset for icon space
        screen.blit(text_surface, text_rect)

        # Save button rect
        button_rects[item] = pygame.Rect(x, y, bar_width, bar_height)

    return button_rects
