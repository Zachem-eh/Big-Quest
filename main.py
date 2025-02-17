import requests
import sys
import pygame
import os


pygame.init()
size = width, height = 600, 450
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Москва')
z_const = 10


def make_request(new_z):
    url = 'https://static-maps.yandex.ru/v1'
    params = {
        'apikey': '4e60121e-3e68-41f0-bd84-eced30775d1c',
        'll': '73.088504,49.807760',
        'z': str(new_z),
    }

    response = requests.get(url, params)
    if not response:
        print(f'{response.status_code} {response.reason}')
        sys.exit(1)

    with open('map.png', mode='wb') as map_file:
        map_file.write(response.content)

    map_image = pygame.image.load('map.png')
    return map_image


map_im = make_request(z_const)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                z_const = z_const + 1 if z_const != 21 else 21
            elif event.key == pygame.K_PAGEDOWN:
                z_const = z_const - 1 if z_const != 0 else 0
            map_im = make_request(z_const)
    screen.blit(map_im, (0, 0))
    pygame.display.flip()

os.remove('map.png')
pygame.quit()
