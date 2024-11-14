# components/walkway.py

import pygame

class Walkway:
    def __init__(self, start_x, start_y, length=200, turn_length=150):
        # Define colors
        self.stanchion_color = (200, 150, 50)  # Gold color for stanchions
        self.rope_color = (200, 0, 0)          # Red color for ropes

        # Define walkway dimensions
        self.length = length       # Straight segment length (vertical)
        self.turn_length = turn_length  # L segment length after the turn (horizontal)

        # Calculate positions for the stanchions along the walkway
        self.stanchions = []
        self.top_stanchions = []     # For top horizontal rope segment
        self.right_stanchions = []   # For vertical right rope segment
        self.left_stanchions = []    # For vertical left rope segment
        self.bottom_stanchions = []  # For bottom horizontal rope segment

        # Add stanchions for the vertical segment going upward (both left and right sides)
        for i in range(0, length + 1, 50):
            left_pos = (start_x, start_y - i)
            right_pos = (start_x + 50, start_y - i)
            self.stanchions.append(left_pos)   # Left stanchions
            self.stanchions.append(right_pos)  # Right stanchions
            self.left_stanchions.append(left_pos)    # For vertical left rope
            self.right_stanchions.append(right_pos)  # For vertical right rope

        # Leave an opening at the top of the vertical section for turning
        turn_start_x = start_x + 50
        turn_start_y = start_y - length

        # Add stanchions for the top horizontal segment
        for j in range(0, turn_length + 1, 50):
            top_pos = (turn_start_x - j, turn_start_y)
            bottom_pos = (turn_start_x - j, turn_start_y + 50)
            self.stanchions.append(top_pos)  # Top stanchions (horizontal)
            self.stanchions.append(bottom_pos)  # Bottom stanchions (horizontal)
            self.top_stanchions.append(top_pos)  # Only top row for horizontal rope
            self.bottom_stanchions.append(bottom_pos)  # Only bottom row for horizontal rope

    def draw(self, screen):
        # Draw stanchions as circles
        for pos in self.stanchions:
            pygame.draw.circle(screen, self.stanchion_color, pos, 10)

        # Draw horizontal ropes between each top stanchion pair
        for i in range(len(self.top_stanchions) - 1):
            pygame.draw.line(screen, self.rope_color, self.top_stanchions[i], self.top_stanchions[i + 1], 4)

        # Draw vertical ropes between each right stanchion pair
        for i in range(len(self.right_stanchions) - 1):
            pygame.draw.line(screen, self.rope_color, self.right_stanchions[i], self.right_stanchions[i + 1], 4)

        # Draw vertical ropes between each left stanchion pair, stopping one stanchion early
        for i in range(len(self.left_stanchions) - 2):
            pygame.draw.line(screen, self.rope_color, self.left_stanchions[i], self.left_stanchions[i + 1], 4)

        # Draw horizontal ropes between each bottom stanchion pair, starting from the second stanchion
        for i in range(1, len(self.bottom_stanchions) - 1):  # Start from the second stanchion
            pygame.draw.line(screen, self.rope_color, self.bottom_stanchions[i], self.bottom_stanchions[i + 1], 4)

        # Entrance arrow pointing up at the bottom of the walkway
        arrow_pos = (self.stanchions[0][0] + 25, self.stanchions[0][1] + 20)
        pygame.draw.polygon(screen, (255, 0, 255), [
            (arrow_pos[0] - 10, arrow_pos[1] + 15),
            (arrow_pos[0] + 10, arrow_pos[1] + 15),
            (arrow_pos[0], arrow_pos[1])
        ])
