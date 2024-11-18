# components/stats.py

import pygame

# Define colors
WHITE = (255, 255, 255)

def draw_stats(screen, money, guests, capacity, security):
    font = pygame.font.SysFont("Arial", 24)
    right_x = screen.get_width() - 70  # Position stats on the right side with some padding
    spacing = 40  # Space between each stat item
    start_y = 40

    # Load the icons from assets
    money_icon = pygame.image.load("assets/moneybag.png").convert_alpha()
    guest_icon = pygame.image.load("assets/people.png").convert_alpha()
    security_icon = pygame.image.load("assets/bouncer.png").convert_alpha()

    # Set icon size and resize all icons
    icon_size = 20
    money_icon = pygame.transform.scale(money_icon, (icon_size, icon_size))
    guest_icon = pygame.transform.scale(guest_icon, (icon_size, icon_size))
    security_icon = pygame.transform.scale(security_icon, (icon_size+5, icon_size+5))

    icon_x = right_x + 10  # Offset for icons to the right of the text

    # Money stat with icon
    money_text = font.render(f"$ {money}", True, WHITE)
    money_rect = money_text.get_rect(right=right_x)
    screen.blit(money_text, (money_rect.x, start_y))
    screen.blit(money_icon, (icon_x, start_y))  # Display money icon

    # Guests stat with icon
    guest_text = font.render(f"{guests}/{capacity}", True, WHITE)
    guest_rect = guest_text.get_rect(right=right_x)
    screen.blit(guest_text, (guest_rect.x, start_y + spacing))
    screen.blit(guest_icon, (icon_x, start_y + spacing))  # Display guest icon

    # Security stat with icon
    security_text = font.render(f"{security}/1", True, WHITE)
    security_rect = security_text.get_rect(right=right_x)
    screen.blit(security_text, (security_rect.x, start_y + 2 * spacing))
    screen.blit(security_icon, (icon_x, start_y + 2 * spacing))  # Display security icon
