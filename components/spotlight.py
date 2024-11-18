import pygame
import math
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Spotlight:
    def __init__(self, x, y, color, angle_offset, num_bulbs=1, bulb_spacing=30, beam_length=300, beam_width=60, rotation_angle=60):
        self.x = x
        self.y = y
        self.color = color
        self.angle_offset = angle_offset
        self.num_bulbs = num_bulbs
        self.bulb_spacing = bulb_spacing
        self.beam_length = beam_length
        self.beam_width = beam_width
        self.rotation_angle = rotation_angle  # Rotation angle for the fixture

    def draw(self, screen):
        # Draw the rotated bar (fixture) for the spotlight
        bar_length = (self.num_bulbs - 1) * self.bulb_spacing + 20
        bar_surface = pygame.Surface((bar_length, 10), pygame.SRCALPHA)
        pygame.draw.rect(bar_surface, (180, 180, 180), (0, 0, bar_length, 10))
        rotated_bar = pygame.transform.rotate(bar_surface, -self.rotation_angle)

        # Position the rotated bar correctly on the screen
        bar_rect = rotated_bar.get_rect(center=(self.x, self.y))
        screen.blit(rotated_bar, bar_rect)

        # Create a surface for the light beam with transparency
        light_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        # Draw only the active bulb and beam based on the rotation angle
        for i in range(self.num_bulbs):
            # Position each bulb along the rotated bar
            bulb_x = self.x - int((self.num_bulbs - 1) * self.bulb_spacing * math.cos(math.radians(self.rotation_angle)) // 2) + i * int(self.bulb_spacing * math.cos(math.radians(self.rotation_angle)))
            bulb_y = self.y + int((self.num_bulbs - 1) * self.bulb_spacing * math.sin(math.radians(self.rotation_angle)) // 2) + i * int(self.bulb_spacing * math.sin(math.radians(self.rotation_angle)))

            # Draw the bulb as a white circle
            pygame.draw.circle(screen, (255, 255, 255), (bulb_x, bulb_y), 8)

            # Calculate beam end points directed toward the dance floor
            end_x = SCREEN_WIDTH // 2 + self.angle_offset
            end_y = SCREEN_HEIGHT // 2

            # Draw the light beam from each bulb
            pygame.draw.polygon(
                light_surface,
                (*self.color, 100),  # Add transparency
                [(bulb_x, bulb_y), (end_x - self.beam_width // 2, end_y), (end_x + self.beam_width // 2, end_y)]
            )

        # Blit the light surface onto the main screen
        screen.blit(light_surface, (0, 0))
