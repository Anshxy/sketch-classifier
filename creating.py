# Program used to generate training data for the model.
import pygame
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DRAWING_AREA = pygame.Rect(50, 50, 700, 500)
BUTTON_RECT = pygame.Rect(50, 10, 100, 30)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Drawing Application')
font = pygame.font.Font(None, 24)
drawing = False
last_pos = None
drawing_color = BLACK
drawing_surface = pygame.Surface((DRAWING_AREA.width, DRAWING_AREA.height))
drawing_surface.fill(WHITE)
counter = 27

def draw_button():
    pygame.draw.rect(screen, GREEN, BUTTON_RECT)
    text = font.render("Save Image", True, WHITE)
    text_rect = text.get_rect(center=BUTTON_RECT.center)
    screen.blit(text, text_rect)

def save_image():
    global counter
    filename = f"square{counter}.png"
    pygame.image.save(drawing_surface, filename)
    print(f"Drawing saved as {filename}")
    #clearing canvas
    drawing_surface.fill(WHITE)
    counter +=1

running = True
while running:

    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if BUTTON_RECT.collidepoint(event.pos):
                save_image()
            else:
                if DRAWING_AREA.collidepoint(event.pos):
                    drawing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            last_pos = None
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                if DRAWING_AREA.collidepoint(event.pos):
                    if last_pos:
                        adjusted_pos = (event.pos[0] - DRAWING_AREA.left, event.pos[1] - DRAWING_AREA.top)
                        last_adjusted_pos = (last_pos[0] - DRAWING_AREA.left, last_pos[1] - DRAWING_AREA.top)
                        pygame.draw.line(drawing_surface, drawing_color, last_adjusted_pos, adjusted_pos, 5)
                    last_pos = event.pos

    screen.blit(drawing_surface, DRAWING_AREA)
    draw_button()
    pygame.display.flip()

pygame.quit()
