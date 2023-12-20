import pygame
import numpy as np
import cv2 as cv
import PIL
import PIL.Image, PIL.ImageDraw
import pickle
import os, os.path
from sklearn.svm import LinearSVC



img_list = np.array([])
class_list = np.array([])

svc = LinearSVC()

# The sample training data is 26 images per class
counter = 26

#circle
for i in range(1, counter + 1):
    img = cv.imread(f"data/circle/circle{i}.png")
    img = cv.resize(img, (50, 50))
    img = img.reshape(-1)
    img_list = np.append(img_list, img)
    class_list = np.append(class_list, 1)

# Square
for i in range(1, counter +1):
    img = cv.imread(f"data/square/square{i}.png")
    img = cv.resize(img, (50, 50))
    img = img.reshape(-1)
    img_list = np.append(img_list, img)
    class_list = np.append(class_list, 2)

# Triangle
for i in range(1, counter + 1):
    img = cv.imread(f"data/triangle/triangle{i}.png")
    img = cv.resize(img, (50, 50))
    img = img.reshape(-1)
    img_list = np.append(img_list, img)
    class_list = np.append(class_list, 3)

# Reshape img_list to maintain the samples count
img_list = img_list.reshape(-1, 2500*3)  

# Fit the SVC model
svc.fit(img_list, class_list)

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

def draw_button():
    pygame.draw.rect(screen, GREEN, BUTTON_RECT)
    text = font.render("Save Image", True, WHITE)
    text_rect = text.get_rect(center=BUTTON_RECT.center)
    screen.blit(text, text_rect)

def save_image():
    pygame.image.save(drawing_surface, 'temp_image.png')  # Save the drawn canvas as an image
    image = cv.imread('temp_image.png')
    image = cv.resize(image, (50, 50)) 
    image = image.reshape(-1)
    prediction = svc.predict([image]) 
    predicted_class = prediction
    print(predicted_class)
    if predicted_class == 1:
        print("circle")
    elif predicted_class == 2:
        print("square")
    elif predicted_class == 3:
        print("triangle")
    os.remove('temp_image.png')  
    
    
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
