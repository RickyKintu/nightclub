import pygame

class Modal:
    def __init__(self, screen, guest):
        self.screen = screen
        self.guest = guest
        self.width = 300
        self.height = 200
        self.bg_color = (50, 50, 50)
        self.text_color = (255, 255, 255)
        self.border_color = (255, 255, 255)
        self.x_button_color = (200, 50, 50)
        self.font = pygame.font.Font(None, 24)

        # Initial position (centered)
        self.x = (screen.get_width() - self.width) // 2
        self.y = (screen.get_height() - self.height) // 2

        # Dragging variables
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0

    def handle_event(self, event):
        """Handle mouse events for dragging and closing."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if self.x + self.width - 40 <= mouse_x <= self.x + self.width - 10 and \
               self.y + 10 <= mouse_y <= self.y + 40:
                # Close button clicked
                return "close"

            # Check if clicking on the top bar for dragging
            if self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + 30:
                self.dragging = True
                self.drag_offset_x = mouse_x - self.x
                self.drag_offset_y = mouse_y - self.y

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # Update modal position while dragging
            self.x = event.pos[0] - self.drag_offset_x
            self.y = event.pos[1] - self.drag_offset_y

        return None

    def draw(self):
        """Draw the modal."""
        # Modal rectangle
        modal_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Draw modal background and border
        pygame.draw.rect(self.screen, self.bg_color, modal_rect)
        pygame.draw.rect(self.screen, self.border_color, modal_rect, 2)

        # Draw "X" button
        x_button_rect = pygame.Rect(self.x + self.width - 40, self.y + 10, 30, 30)
        pygame.draw.rect(self.screen, self.x_button_color, x_button_rect)
        x_text = self.font.render("X", True, self.text_color)
        self.screen.blit(x_text, (x_button_rect.x + 8, x_button_rect.y + 5))

        # Draw guest image
        image_x = self.x + 20
        image_y = self.y + 50
        guest_image = self.guest.frames["down"][0]  # Show the first frame as the guest image
        self.screen.blit(guest_image, (image_x, image_y))

        # Draw guest info
        info_x = image_x + 50
        info_y = image_y
        info_lines = [
            f"Guest ID: {id(self.guest)}",
            f"Position: ({int(self.guest.x)}, {int(self.guest.y)})"
        ]
        for line in info_lines:
            text_surface = self.font.render(line, True, self.text_color)
            self.screen.blit(text_surface, (info_x, info_y))
            info_y += 30

        return x_button_rect
