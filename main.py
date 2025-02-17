import requests
import sys
import pygame
import os


pygame.init()
size = width, height = 600, 450
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Москва')


url = 'https://static-maps.yandex.ru/v1'
params = {
    'apikey': '4e60121e-3e68-41f0-bd84-eced30775d1c',
    'll': '73.088504,49.807760',
    'z': '10',
}

response = requests.get(url, params)
if not response:
    print(f'{response.status_code} {response.reason}')
    sys.exit(1)

with open('map.png', mode='wb') as map_file:
    map_file.write(response.content)

running = True
map_im = pygame.image.load('map.png')
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(map_im, (0, 0))
    pygame.display.flip()

os.remove('map.png')
pygame.quit()
