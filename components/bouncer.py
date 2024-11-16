import pygame

class Bouncer:
    def __init__(self, x, y, sprite_sheet):
        """
        Represents a Bouncer at the end of the walkway.
        :param x: X position of the Bouncer.
        :param y: Y position of the Bouncer.
        :param sprite_sheet: The sprite sheet image for the Bouncer.
        """
        self.x = x
        self.y = y
        self.speed = 0  # Bouncers don't move by default
        self.current_direction = "down"
        self.current_frame = 0
        self.frame_duration = 10
        self.frame_timer = 0
        self.is_moving = False

        # Load sprite sheet and initialize frames for each direction
        self.frames = {
            "up": self.extract_frames(sprite_sheet, 152),
            "down": self.extract_frames(sprite_sheet, 8),
            "left": self.extract_frames(sprite_sheet, 57),
            "right": self.extract_frames(sprite_sheet, 105),
        }

    def extract_frames(self, sprite_sheet, y_offset):
        """
        Extract frames for a given direction from the sprite sheet.
        :param sprite_sheet: The sprite sheet image.
        :param y_offset: The vertical offset for the direction's animation frames.
        :return: A list of frames for the given direction.
        """
        frames = []
        frame_width = 32
        frame_height = 40
        initial_x_offset = 8
        for i in range(4):
            x = initial_x_offset + i * (frame_width + 16)
            frame = sprite_sheet.subsurface((x, y_offset, frame_width, frame_height)).copy()
            frames.append(frame)
        return frames

    def update_animation(self):
        """
        Update the animation frames of the Bouncer.
        """
        self.frame_timer += 1
        if self.frame_timer >= self.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.frames[self.current_direction])
            self.frame_timer = 0

    def draw(self, screen):
        """
        Draw the Bouncer on the screen.
        :param screen: The Pygame screen object.
        """
        current_image = self.frames[self.current_direction][self.current_frame]
        screen.blit(current_image, (int(self.x) - 16, int(self.y) - 20))  # Adjust to center
        self.update_animation()
