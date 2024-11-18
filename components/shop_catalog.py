import pygame
from components.bouncer import Bouncer
from components.walkway import Walkway


class ShopCatalog:
    def __init__(self, screen, categories, money_ref, bouncer_sprite, walkway, bouncers_ref):
        """
        Initialize the shop catalog.
        :param screen: The screen to render the catalog on.
        :param categories: A dictionary with category names as keys and item lists as (name, price) tuples.
        :param money_ref: A mutable reference to the player's money.
        :param bouncer_sprite: The sprite for the Bouncer character.
        :param walkway: A reference to the Walkway object for Bouncer placement.
        :param bouncers_ref: A reference to the list of Bouncers in the game.
        """
        self.screen = screen
        self.categories = categories
        self.money_ref = money_ref  # Reference to money
        self.bouncer_sprite = bouncer_sprite
        self.walkway = walkway
        self.bouncers_ref = bouncers_ref  # Reference to the list of bouncers
        self.current_category = None  # Start with no category selected
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 48)
        self.bg_color = (50, 50, 50)  # Background color
        self.text_color = (255, 255, 255)  # Text color
        self.button_color = (100, 100, 255)  # Button background color
        self.hover_color = (150, 150, 255)  # Hover effect
        self.items_hover_color = (200, 200, 255)  # Hover color for items
        self.item_buttons = []  # Store item buttons for hover detection
        self.button_padding = 10
        self.back_button_rect = None  # "Back" button rectangle
        self.close_button_rect = None  # "Close" button rectangle

        # Initialize the category buttons
        self.category_buttons = []
        self.init_category_buttons()

    def init_category_buttons(self):
        """Create buttons for each category."""
        x, y = 50, 100
        for category in self.categories:
            button_rect = pygame.Rect(x, y, 200, 50)
            self.category_buttons.append((category, button_rect))
            y += 60

    def draw(self):
        """Draw the shop catalog."""
        self.screen.fill(self.bg_color)

        # Margin settings
        top_margin = 30
        between_margin = 20
        bottom_margin = 40

        # Draw title with margin
        title_text = self.title_font.render("Shop Catalog", True, self.text_color)
        self.screen.blit(
            title_text,
            (self.screen.get_width() // 2 - title_text.get_width() // 2, top_margin)
        )

        mouse_x, mouse_y = pygame.mouse.get_pos()

        if self.current_category is None:
            # Draw category buttons with proper margins
            button_y_start = top_margin + title_text.get_height() + between_margin
            for category, button_rect in self.category_buttons:
                is_hovered = button_rect.collidepoint(mouse_x, mouse_y)
                color = self.hover_color if is_hovered else self.button_color

                # Adjust button position with margins
                button_rect.y = button_y_start
                pygame.draw.rect(self.screen, color, button_rect)
                text_surface = self.font.render(category, True, self.text_color)
                text_x = button_rect.x + (button_rect.width - text_surface.get_width()) // 2
                text_y = button_rect.y + (button_rect.height - text_surface.get_height()) // 2
                self.screen.blit(text_surface, (text_x, text_y))
                button_y_start += button_rect.height + between_margin
        else:
            # Draw items for the selected category with margins
            category_title = self.title_font.render(self.current_category, True, self.text_color)
            self.screen.blit(category_title, (50, top_margin + title_text.get_height() + between_margin))

            items = self.categories[self.current_category]
            self.item_buttons = []  # Clear and recreate item buttons
            y = top_margin + title_text.get_height() + between_margin * 3
            for item_name, item_price in items:
                item_rect = pygame.Rect(100, y, 300, 40)
                is_hovered = item_rect.collidepoint(mouse_x, mouse_y)
                color = self.items_hover_color if is_hovered else self.bg_color

                pygame.draw.rect(self.screen, color, item_rect)
                item_text = f"{item_name} - ${item_price}"
                item_surface = self.font.render(item_text, True, self.text_color)
                self.screen.blit(item_surface, (item_rect.x + 10, item_rect.y + 5))
                self.item_buttons.append(((item_name, item_price), item_rect))
                y += item_rect.height + between_margin

            # Draw "Back" button with bottom margin
            back_button_rect = pygame.Rect(
                50,
                self.screen.get_height() - bottom_margin - 40,
                100,
                40
            )
            pygame.draw.rect(self.screen, self.button_color, back_button_rect)
            back_text = self.font.render("Back", True, self.text_color)
            self.screen.blit(back_text, (back_button_rect.x + 15, back_button_rect.y + 5))
            self.back_button_rect = back_button_rect

        # Draw "Close" button at the top-right corner
        close_button_rect = pygame.Rect(self.screen.get_width() - 150, top_margin, 100, 40)
        pygame.draw.rect(self.screen, self.button_color, close_button_rect)
        close_text = self.font.render("Close", True, self.text_color)
        self.screen.blit(close_text, (close_button_rect.x + 10, close_button_rect.y + 5))
        self.close_button_rect = close_button_rect

        # Display the player's current money in the bottom-right corner
        money_text = self.font.render(f"Money: ${self.money_ref[0]}", True, (0, 255, 0))  # Green color
        money_text_rect = money_text.get_rect(
            bottomright=(self.screen.get_width() - 20, self.screen.get_height() - 20)
        )
        self.screen.blit(money_text, money_text_rect)




    def handle_event(self, event):
        """Handle mouse and keyboard events in the shop."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_pos = event.pos

            # Handle "Close" button
            if self.close_button_rect and self.close_button_rect.collidepoint(mouse_pos):
                return "close"

            # Handle "Back" button
            if self.back_button_rect and self.back_button_rect.collidepoint(mouse_pos):
                self.current_category = None  # Go back to the main categories
                return

            # Handle item selection
            if self.current_category:
                for (item_name, item_price), item_rect in self.item_buttons:
                    if item_rect.collidepoint(mouse_pos):
                        # Check if the player has enough money
                        if self.money_ref[0] >= item_price:
                            print(f"Purchased: {item_name} for ${item_price}")
                            self.money_ref[0] -= item_price

                            # Add the Bouncer if purchased
                            if item_name == "Bouncer":
                                bouncer_position = self.walkway.stanchions[-1]
                                self.bouncers_ref.append(Bouncer(
                                x=bouncer_position[0] - 30,
                                y=bouncer_position[1],
                                sprite_sheet=self.bouncer_sprite  # Correct parameter
                            ))
                        else:
                            print("Not enough money!")
                        return

            # Handle category selection
            if self.current_category is None:
                for category, button_rect in self.category_buttons:
                    if button_rect.collidepoint(mouse_pos):
                        self.current_category = category  # Open the selected category
                        return

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Close catalog with ESC key
                return "close"

        return None
