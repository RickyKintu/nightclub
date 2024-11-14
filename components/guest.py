# components/guest.py

import pygame
import math

class Guest:
    def __init__(self, start_x, start_y, waypoints):
        self.x = start_x
        self.y = start_y
        self.waypoints = waypoints  # List of waypoints to follow
        self.current_waypoint = 0   # Start at the first waypoint
        self.speed = 2  # Adjust speed as needed

    def move(self):
        if self.current_waypoint < len(self.waypoints):
            # Get the target waypoint position
            target_x, target_y = self.waypoints[self.current_waypoint]
            
            # Calculate direction vector toward the waypoint
            direction_x = target_x - self.x
            direction_y = target_y - self.y
            distance = math.hypot(direction_x, direction_y)
            
            # Move toward the waypoint if not already there
            if distance > self.speed:
                # Normalize the direction vector and move
                self.x += self.speed * (direction_x / distance)
                self.y += self.speed * (direction_y / distance)
            else:
                # Move to the waypoint and switch to the next one
                self.x, self.y = target_x, target_y
                self.current_waypoint += 1

    def draw(self, screen):
        # Draw the guest as a simple circle
        pygame.draw.circle(screen, (0, 255, 0), (int(self.x), int(self.y)), 10)  # Green color for guest
