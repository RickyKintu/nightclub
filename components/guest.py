import pygame
import math
import random
from components.chat_bubble import ChatBubble

class Guest:
    def __init__(self, start_x, start_y, waypoints, sprite_sheet, get_random_dance_floor_tile):
        self.x = start_x
        self.y = start_y
        self.waypoints = waypoints
        self.current_waypoint = 0
        self.speed = 3
        self.free_movement = False  # Flag for free movement after waypoints
        self.pause_timer = 0  # Timer for pausing
        self.target_location = None  # Target location for free movement
        self.get_random_dance_floor_tile = get_random_dance_floor_tile
        self.selected = False  # New: Track if the guest is selected

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

        self.chat_bubble = None  # Chat bubble for guest's needs
        self.need_state = None  # Current need state
        self.need_timer = random.randint(300, 600)  # Timer to trigger a need


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
        # Stop movement if the guest is selected
        if self.selected:
            self.is_moving = False
            self.current_frame = 0  # Reset animation to the first frame when stationary
            return

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

    def update_need(self, bubble_images):
        """
        Update the guest's need state and assign a chat bubble if necessary.
        :param bubble_images: Dictionary of images for different needs.
        """
        self.need_timer -= 1
        if self.need_timer <= 0:
            # Randomly assign a need state
            self.need_state = random.choice(["thirsty", "toilet", "hungry"])
            self.chat_bubble = ChatBubble(self, bubble_images[self.need_state])
            self.need_timer = random.randint(300, 600)  # Reset timer

        if self.chat_bubble:
            self.chat_bubble.update()  # Update the visibility of the chat bubble

    def clear_need(self):
        """Clear the guest's current need and remove the chat bubble."""
        self.need_state = None
        self.chat_bubble = None

    def draw(self, screen, is_selected=False, is_faded=False):
        # Draw the guest sprite
        current_image = self.frames[self.current_direction][self.current_frame]
        guest_rect = pygame.Rect(int(self.x) - 16, int(self.y) - 20, 32, 40)

        if is_faded:
            # Create a surface for the faded guest
            faded_surface = pygame.Surface((32, 40), pygame.SRCALPHA)  # Match guest size
            faded_surface.blit(current_image, (0, 0))  # Blit the sprite onto the surface
            faded_surface.set_alpha(100)  # Set transparency (100 out of 255)
            screen.blit(faded_surface, guest_rect.topleft)  # Blit the faded surface
        else:
            screen.blit(current_image, guest_rect.topleft)  # Draw normally

        # Draw a highlight border if the guest is selected
        if is_selected:
            pygame.draw.rect(screen, (255, 255, 0), guest_rect, 3)  # Yellow border for selection

        # Draw the chat bubble if it exists
        if self.chat_bubble:
            self.chat_bubble.draw(screen)


    def is_clicked(self, mouse_pos):
        """Check if the guest is clicked."""
        guest_rect = pygame.Rect(int(self.x) - 16, int(self.y) - 20, 32, 40)  # Guest's clickable area
        return guest_rect.collidepoint(mouse_pos)
