from settings import *


class Button:
    def __init__(self, x, y, font, images: dict, callback: lambda: None, text=None):
        self.rect = images["normal"].get_rect(center=(x, y))
        self.text = text
        self.font = font
        self.images = images
        self.callback = callback
        self.state = "normal"

    def handle_event(self, event: pygame.event.Event):
        """Handle mouse events"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.state = "click"
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.state == "click" and self.rect.collidepoint(event.pos):
                self.callback()
            self.state = "normal"

    def update(self):
        """Update the button state"""
        if self.state != "click":
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.state = "hover"
            else:
                self.state = "normal"

    def draw(self, screen: pygame.Surface):
        """Draw the button"""
        image = self.images[self.state]
        screen.blit(image, self.rect)

        # Vẽ văn bản
        if self.text is not None:
            text_surface = self.font.render(self.text, True, COLOR["black"])
            text_rect = text_surface.get_rect(
                center=(self.rect.centerx, self.rect.centery+3))
            screen.blit(text_surface, text_rect)


class Waiting_Interface:
    def __init__(self, images, font):
        self.font = font
        self.images = images

        # Initialize buttons
        self.buttons: list[Button] = []
        middle = CELL_NUMBER * CELL_SIZE / 2
        self.buttons.append(Button(
            middle, middle,
            text="New game",
            font=self.font,
            images=self.images,
            callback=lambda: (pygame.quit(), exit())
        ))
        self.buttons.append(Button(
            middle, middle + 50,
            text="Back to game",
            font=self.font,
            images=self.images,
            callback=lambda: (pygame.quit(), exit())
        ))
        self.buttons.append(Button(
            middle, middle + 100,
            text="Restart",
            font=self.font,
            images=self.images,
            callback=lambda: (pygame.quit(), exit())
        ))
        self.buttons.append(Button(
            middle, middle + 150,
            text="Quit game",
            font=self.font,
            images=self.images,
            callback=lambda: (pygame.quit(), exit())
        ))

    def draw(self, surface, status_win: bool = False, font_txt_win: pygame.font.Font = None):
        # Draw overlay
        overlay = pygame.Surface(surface.get_size())
        overlay.fill(COLOR["black"])
        overlay.set_alpha(ALPHA_VALUE_OVERLAY)
        surface.blit(overlay, (0, 0))

        middle = CELL_NUMBER * CELL_SIZE / 2

        # Draw text
        if status_win:
            victory_text = font_txt_win.render(
                "Victory!", True, COLOR["white"])
            surface.blit(victory_text, victory_text.get_rect(
                center=(middle, middle - 100)))

        # Draw buttons
        for button in self.buttons:
            button.update()
            button.draw(surface)

    def handle_event(self, event):
        """Handle mouse events"""
        for button in self.buttons:
            button.handle_event(event)
