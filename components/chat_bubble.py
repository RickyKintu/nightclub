import pygame
import random

class ChatBubble:
    def __init__(self, guest, image, offset_y=20):
        """
        Represents a chat bubble above a guest.
        :param guest: The guest the chat bubble is attached to.
        :param image: The image to display inside the bubble.
        :param offset_y: Offset in pixels above the guest's position.
        """
        self.guest = guest
        self.image = image
        self.offset_y = offset_y
        self.visible = False  # Start invisible
        self.timer = random.randint(30, 100)  # Time until visibility toggles
        self.padding = 10  # Padding around the image inside the bubble
        self.bubble_color = (255, 255, 255)  # White background for the bubble
        self.border_color = (0, 0, 0)  # Black border for the bubble
        self.border_width = 2  # Thickness of the border
        self.corner_radius = 15  # Rounded corner radius

    def update(self):
        """Update the visibility of the chat bubble based on the timer."""
        self.timer -= 1
        if self.timer <= 0:
            self.visible = not self.visible  # Toggle visibility
            self.timer = random.randint(100, 150)  # Reset the timer

    def draw(self, screen):
        """Draw the chat bubble above the guest if visible."""
        if not self.visible:
            return

        # Calculate the position and size of the bubble
        bubble_width = self.image.get_width() + self.padding * 2
        bubble_height = self.image.get_height() + self.padding * 2
        bubble_x = int(self.guest.x) - bubble_width // 2
        bubble_y = int(self.guest.y) - self.offset_y - bubble_height

        # Draw the rounded rectangle for the bubble background
        bubble_rect = pygame.Rect(bubble_x, bubble_y, bubble_width, bubble_height)
        pygame.draw.rect(screen, self.bubble_color, bubble_rect, border_radius=self.corner_radius)

        # Draw the border around the bubble
        pygame.draw.rect(screen, self.border_color, bubble_rect, self.border_width, border_radius=self.corner_radius)

        # Draw the image inside the bubble
        image_x = bubble_x + self.padding
        image_y = bubble_y + self.padding
        screen.blit(self.image, (image_x, image_y))
