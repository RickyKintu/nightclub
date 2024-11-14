import pygame
import sys

# Initiera Pygame
pygame.init()

# Fönsterinställningar
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Nattklubbsspel - Nivå 1")

# Färger
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

def draw_dance_floor():
    # Justerade hörnpunkter för parallellogrammet åt andra hållet
    top_left = (300, 150)
    top_right = (500, 150)
    bottom_right = (450, 350)
    bottom_left = (250, 350)

    # Rita parallellogrammets yta
    pygame.draw.polygon(screen, GRAY, [top_left, top_right, bottom_right, bottom_left])

    # Lägg till ett mer detaljerat rutmönster inuti parallellogrammet
    rows = 10  # Antal horisontella linjer
    cols = 10  # Antal vertikala linjer
    
    # Horisontella linjer som är parallella med toppen och botten
    for j in range(1, rows):
        start_x = top_left[0] + j * (bottom_left[0] - top_left[0]) // rows
        start_y = top_left[1] + j * (bottom_left[1] - top_left[1]) // rows
        end_x = top_right[0] + j * (bottom_right[0] - top_right[0]) // rows
        end_y = top_right[1] + j * (bottom_right[1] - top_right[1]) // rows
        pygame.draw.line(screen, WHITE, (start_x, start_y), (end_x, end_y), 1)

    # Vertikala linjer som är parallella med vänster- och högersidan
    for i in range(1, cols):
        start_x = top_left[0] + i * (top_right[0] - top_left[0]) // cols
        start_y = top_left[1]
        end_x = bottom_left[0] + i * (bottom_right[0] - bottom_left[0]) // cols
        end_y = bottom_left[1]
        pygame.draw.line(screen, WHITE, (start_x, start_y), (end_x, end_y), 1)



def draw_speakers():
    speaker_color = (50, 50, 50)
    # Flytta högtalarna åt vänster för att centrera dem ovanför dansgolvet
    pygame.draw.rect(screen, speaker_color, pygame.Rect(350, 100, 40, 40))  # Första högtalaren
    pygame.draw.rect(screen, speaker_color, pygame.Rect(410, 100, 40, 40))  # Andra högtalaren

def draw_speakers_and_dj():
    speaker_color = (50, 50, 50)
    dj_color = (200, 100, 50)  # Färg för DJ:n
    table_color = (100, 100, 100)  # Färg för DJ-bordet

    # Flytta högtalarna längre ut åt sidorna
    pygame.draw.rect(screen, speaker_color, pygame.Rect(330, 100, 40, 40))  # Första högtalaren
    pygame.draw.rect(screen, speaker_color, pygame.Rect(430, 100, 40, 40))  # Andra högtalaren

    # Lägg till ett DJ-bord mellan högtalarna
    pygame.draw.rect(screen, table_color, pygame.Rect(370, 110, 60, 20))  # DJ-bordet

    # Lägg till en DJ-figur bakom bordet (en enkel cirkel som huvudet och en rektangel som kroppen)
    pygame.draw.circle(screen, dj_color, (400, 85), 10)  # Huvudet
    pygame.draw.rect(screen, dj_color, pygame.Rect(395, 95, 10, 15))  # Kroppen



# Startar spel-loopen
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # Rita nattklubbens element
    draw_dance_floor()
    draw_speakers_and_dj()

    pygame.display.flip()

pygame.quit()
sys.exit()
