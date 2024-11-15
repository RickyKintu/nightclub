import pygame

class Walkway:
    def __init__(self, start_x, start_y, length=200, turn_length=150):
        # Define colors
        self.stanchion_color = (200, 150, 50)
        self.rope_color = (200, 0, 0)

        # Define walkway dimensions
        self.length = length  # Vertical segment length
        self.turn_length = turn_length  # Horizontal segment length (after turn)

        # Store starting x and y coordinates
        self.start_x = start_x
        self.start_y = start_y

        # Calculate stanchion positions (for visual purposes)
        self.stanchions = []
        self.top_stanchions = []
        self.right_stanchions = []
        self.left_stanchions = []
        self.bottom_stanchions = []

        # Add stanchions for the vertical segment going upward
        for i in range(0, length + 1, 50):
            left_pos = (start_x, start_y - i)
            right_pos = (start_x + 50, start_y - i)
            self.stanchions.append(left_pos)
            self.stanchions.append(right_pos)
            self.left_stanchions.append(left_pos)
            self.right_stanchions.append(right_pos)

        # Add stanchions for the top horizontal segment
        turn_start_x = start_x + 50
        turn_start_y = start_y - length
        for j in range(0, turn_length + 1, 50):
            top_pos = (turn_start_x - j, turn_start_y)
            bottom_pos = (turn_start_x - j, turn_start_y + 50)
            self.stanchions.append(top_pos)
            self.stanchions.append(bottom_pos)
            self.top_stanchions.append(top_pos)
            self.bottom_stanchions.append(bottom_pos)

    def draw(self, screen):
        # Draw stanchions as circles
        for pos in self.stanchions:
            pygame.draw.circle(screen, self.stanchion_color, pos, 10)

        # Draw ropes as lines
        for i in range(len(self.top_stanchions) - 1):
            pygame.draw.line(screen, self.rope_color, self.top_stanchions[i], self.top_stanchions[i + 1], 4)
        for i in range(len(self.right_stanchions) - 1):
            pygame.draw.line(screen, self.rope_color, self.right_stanchions[i], self.right_stanchions[i + 1], 4)
        for i in range(len(self.left_stanchions) - 2):
            pygame.draw.line(screen, self.rope_color, self.left_stanchions[i], self.left_stanchions[i + 1], 4)
        for i in range(1, len(self.bottom_stanchions) - 1):
            pygame.draw.line(screen, self.rope_color, self.bottom_stanchions[i], self.bottom_stanchions[i + 1], 4)

