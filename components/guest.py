import pygame
import math
import random

class Guest:
    def __init__(self, start_x, start_y, waypoints, sprite_sheet, get_random_dance_floor_tile):
        self.x = start_x
        self.y = start_y
        self.waypoints = waypoints
        self.current_waypoint = 0
        self.speed = 2
        self.free_movement = False  # Flag for free movement after waypoints
        self.pause_timer = 0  # Timer for pausing
        self.target_location = None  # Target location for free movement
        self.get_random_dance_floor_tile = get_random_dance_floor_tile

        # Load sprite sheet and initialize frames for each direction
        self.frames = {
            "up": self.extract_frames(sprite_sheet, 152),
            "down": self.extract_frames(sprite_sheet, 8),
            "left": self.extract_frames(sprite_sheet, 57),
            "right": self.extract_frames(sprite_sheet, 105)
        }
        self.current_direction = "down"
        self.current_frame = 0
        self.frame_duration = 10
        self.frame_timer = 0
        self.is_moving = False  # Tracks if the guest is currently moving

    def extract_frames(self, sprite_sheet, y_offset):
        frames = []
        frame_width = 32
        frame_height = 40
        initial_x_offset = 8
        for i in range(4):
            x = initial_x_offset + i * (frame_width + 16)
            frame = sprite_sheet.subsurface((x, y_offset, frame_width, frame_height)).copy()
            frames.append(frame)
        return frames

    def update_direction(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        if abs(dx) > abs(dy):
            self.current_direction = "right" if dx > 0 else "left"
        else:
            self.current_direction = "down" if dy > 0 else "up"

    def move(self):
        self.is_moving = False  # Assume the guest is stationary unless movement occurs

        if not self.free_movement:
            if self.current_waypoint < len(self.waypoints):
                # Move toward the next waypoint
                target_x, target_y = self.waypoints[self.current_waypoint]
                self.update_direction(target_x, target_y)
                direction_x = target_x - self.x
                direction_y = target_y - self.y
                distance = math.hypot(direction_x, direction_y)

                if distance > self.speed:
                    self.x += self.speed * (direction_x / distance)
                    self.y += self.speed * (direction_y / distance)
                    self.is_moving = True
                else:
                    self.x, self.y = target_x, target_y
                    self.current_waypoint += 1
            else:
                # Enable free movement within the dance floor bounds
                self.free_movement = True
                self.pause_timer = random.randint(60, 120)  # Initial pause before first random move

        elif self.free_movement:
            if self.pause_timer > 0:
                # Pausing logic
                self.pause_timer -= 1
            else:
                if self.target_location is None:
                    # Pick a new random target location within the dance floor
                    self.target_location = self.get_random_dance_floor_tile()
                else:
                    # Move toward the random target location
                    target_x, target_y = self.target_location
                    self.update_direction(target_x, target_y)
                    direction_x = target_x - self.x
                    direction_y = target_y - self.y
                    distance = math.hypot(direction_x, direction_y)

                    if distance > self.speed:
                        self.x += self.speed * (direction_x / distance)
                        self.y += self.speed * (direction_y / distance)
                        self.is_moving = True
                    else:
                        # Reached the target location, pause again
                        self.target_location = None
                        self.pause_timer = random.randint(60, 120)

        # Update frame for animation only if the guest is moving
        if self.is_moving:
            self.frame_timer += 1
            if self.frame_timer >= self.frame_duration:
                self.current_frame = (self.current_frame + 1) % len(self.frames[self.current_direction])
                self.frame_timer = 0
        else:
            self.current_frame = 0  # Reset animation to the first frame when not moving

    def draw(self, screen):
        current_image = self.frames[self.current_direction][self.current_frame]
        screen.blit(current_image, (int(self.x) - 16, int(self.y) - 20))  # Adjust to center
