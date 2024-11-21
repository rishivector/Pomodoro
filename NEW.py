import pygame
import sys
from tkinter import Tk, messagebox

pygame.init()

# Fullscreen setup
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = pygame.display.get_surface().get_size()
pygame.display.set_caption("Customizable Pomodoro Timer")
CLOCK = pygame.time.Clock()

BACKDROP = pygame.image.load("assets/backdrop.png")
WHITE_BUTTON = pygame.image.load("assets/button.png")
FONT = pygame.font.Font("assets/ArialRoundedMTBold.ttf", 120)

class Button:
    def __init__(self, surface=None, pos=None, width=None, height=None, text_input=None, font=None, base_color=None, hovering_color=None):
        self.surface = surface
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.width = width
        self.height = height
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.surface is None:
            self.surface = self.text
        else:
            self.surface = pygame.transform.smoothscale(self.surface, (width, height))
        self.rect = self.surface.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.surface is not None:
            screen.blit(self.surface, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def change_color(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

POMODORO_LENGTH = 1500
SHORT_BREAK_LENGTH = 300
LONG_BREAK_LENGTH = 900

current_seconds = POMODORO_LENGTH
default_seconds = POMODORO_LENGTH
pygame.time.set_timer(pygame.USEREVENT, 1000)
started = False

INPUT_BOX = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 250, 200, 40)
user_text = ""
input_active = False

START_STOP_BUTTON = Button(WHITE_BUTTON, (WIDTH / 2 - 120, HEIGHT / 2 + 150), 170, 60, "START",
                           pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#c97676", "#9ab034")
RESET_BUTTON = Button(WHITE_BUTTON, (WIDTH / 2 + 120, HEIGHT / 2 + 150), 170, 60, "RESET",
                      pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#c97676", "#9ab034")
POMODORO_BUTTON = Button(None, (WIDTH / 2 - 200, HEIGHT / 2 - 140), 140, 40, "Pomodoro",
                         pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#9ab034")
SHORT_BREAK_BUTTON = Button(None, (WIDTH / 2, HEIGHT / 2 - 140), 140, 40, "Short Break",
                            pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#9ab034")
LONG_BREAK_BUTTON = Button(None, (WIDTH / 2 + 200, HEIGHT / 2 - 140), 140, 40, "Long Break",
                           pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#9ab034")

def show_notification(message):
    root = Tk()
    root.withdraw()
    messagebox.showinfo("Pomodoro Timer", message)
    root.destroy()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if START_STOP_BUTTON.check_for_input(pygame.mouse.get_pos()):
                started = not started
            if RESET_BUTTON.check_for_input(pygame.mouse.get_pos()):
                current_seconds = default_seconds
                started = False
            if POMODORO_BUTTON.check_for_input(pygame.mouse.get_pos()):
                current_seconds = POMODORO_LENGTH
                default_seconds = POMODORO_LENGTH
                started = False
            if SHORT_BREAK_BUTTON.check_for_input(pygame.mouse.get_pos()):
                current_seconds = SHORT_BREAK_LENGTH
                default_seconds = SHORT_BREAK_LENGTH
                started = False
            if LONG_BREAK_BUTTON.check_for_input(pygame.mouse.get_pos()):
                current_seconds = LONG_BREAK_LENGTH
                default_seconds = LONG_BREAK_LENGTH
                started = False
            if INPUT_BOX.collidepoint(event.pos):
                input_active = True
            else:
                input_active = False
            START_STOP_BUTTON.text_input = "STOP" if started else "START"
            START_STOP_BUTTON.text = pygame.font.Font("assets/ArialRoundedMTBold.ttf", 20).render(
                START_STOP_BUTTON.text_input, True, START_STOP_BUTTON.base_color)
        if event.type == pygame.USEREVENT and started:
            current_seconds -= 1
            if current_seconds == 0:
                started = False
                show_notification("Time's up!")

        if event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_RETURN:
                    try:
                        mins, secs = map(int, user_text.split(":"))
                        custom_seconds = mins * 60 + secs
                        current_seconds = custom_seconds
                        default_seconds = custom_seconds
                        user_text = ""
                    except ValueError:
                        user_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

    SCREEN.fill("#ba4949")
    SCREEN.blit(BACKDROP, BACKDROP.get_rect(center=(WIDTH / 2, HEIGHT / 2)))

    START_STOP_BUTTON.update(SCREEN)
    START_STOP_BUTTON.change_color(pygame.mouse.get_pos())
    RESET_BUTTON.update(SCREEN)
    RESET_BUTTON.change_color(pygame.mouse.get_pos())
    POMODORO_BUTTON.update(SCREEN)
    POMODORO_BUTTON.change_color(pygame.mouse.get_pos())
    SHORT_BREAK_BUTTON.update(SCREEN)
    SHORT_BREAK_BUTTON.change_color(pygame.mouse.get_pos())
    LONG_BREAK_BUTTON.update(SCREEN)
    LONG_BREAK_BUTTON.change_color(pygame.mouse.get_pos())

    pygame.draw.rect(SCREEN, "#FFFFFF" if input_active else "#AAAAAA", INPUT_BOX)
    input_text_surface = pygame.font.Font(None, 32).render(user_text, True, "black")
    SCREEN.blit(input_text_surface, (INPUT_BOX.x + 5, INPUT_BOX.y + 5))
    # input_label = pygame.font.Font(None, 32).render("Enter Time (MIN:SEC):", True, "white")
    # SCREEN.blit(input_label, (INPUT_BOX.x, INPUT_BOX.y + 50))

    if current_seconds >= 0:
        display_seconds = current_seconds % 60
        display_minutes = int(current_seconds / 60) % 60
    timer_text = FONT.render(f"{display_minutes:02}:{display_seconds:02}", True, "white")
    SCREEN.blit(timer_text, timer_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 25)))

    # Draw the progress bar
    progress_width = int((current_seconds / default_seconds) * (WIDTH - 200)) if default_seconds > 0 else 0
    pygame.draw.rect(SCREEN, "#555555", (100, HEIGHT - 50, WIDTH - 200, 20))  # Background bar
    pygame.draw.rect(SCREEN, "#9ab034", (100, HEIGHT - 50, progress_width, 20))  # Filled progress

    pygame.display.update()
