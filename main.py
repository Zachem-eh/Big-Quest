import requests
import sys
import pygame
import os


pygame.init()
size = width, height = 600, 450
FPS = 60
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Москва')
all_sprites = pygame.sprite.Group()
theme_group = pygame.sprite.Group()
z_const = 10
coord = ['73.088504', '49.807760']
theme = 'light'
moving_long = {0: 100.0, 1: 50.0, 2: 25.0, 3: 12.5, 4: 6.25, 5: 3.125, 6: 1.5625, 7: 0.78125, 8: 0.390625,
               9: 0.1953125, 10: 0.09765625, 11: 0.048828125, 12: 0.0244140625, 13: 0.01220703125,
               14: 0.006103515625, 15: 0.0030517578125, 16: 0.00152587890625, 17: 0.000762939453125,
               18: 0.0003814697265625, 19: 0.00019073486328125, 20: 9.5367431640625e-05, 21: 4.76837158203125e-05}
moving_lat = {0: 30.0, 1: 15.0, 2: 7.51, 3: 3, 4: 1.875, 5: 0.9375, 6: 0.46875, 7: 0.234375, 8: 0.1171875,
              9: 0.05859375, 10: 0.029296875, 11: 0.0146484375, 12: 0.00732421875, 13: 0.003662109375,
              14: 0.0018310546875, 15: 0.00091552734375, 16: 0.000457763671875, 17: 0.0002288818359375,
              18: 0.00011444091796875, 19: 5.7220458984375e-05, 20: 2.86102294921875e-05, 21: 1.430511474609375e-05}


def make_request_map(new_z, new_ll, new_theme, obj_ll=None):
    url = 'https://static-maps.yandex.ru/v1'
    if not obj_ll:
        params = {
            'apikey': '4e60121e-3e68-41f0-bd84-eced30775d1c',
            'll': ','.join(new_ll),
            'z': str(new_z),
            'theme': new_theme
        }
    else:
        global z_const, coord
        coord = obj_ll
        z_const = 10
        params = {
            'apikey': '4e60121e-3e68-41f0-bd84-eced30775d1c',
            'll': ','.join(obj_ll),
            'z': str(z_const),
            'theme': new_theme
        }

    response = requests.get(url, params)
    if not response:
        print(f'{response.status_code} {response.reason}')
        sys.exit(1)

    with open('map.png', mode='wb') as map_file:
        map_file.write(response.content)

    map_image = pygame.image.load('map.png')
    return map_image


def make_request_pos(text):
    url = 'https://geocode-maps.yandex.ru/1.x'
    params = {
        'apikey': '957cd94a-71cc-4433-8fbf-279c95c506aa',
        'geocode': text,
        'lang': 'ru_RU',
        'format': 'json'
    }

    response = requests.get(url=url, params=params)

    if not response:
        print(f'{response.status_code} {response.reason}')
        return None
    else:
        data = response.json()
        feature = data['response']['GeoObjectCollection']['featureMember']
        if feature:
            pos = feature[0]['GeoObject']['Point']['pos'].split()
            return pos
        else:
            return None


class InputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, text=''):
        super().__init__(all_sprites)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(x, y, w, h)
        self.image.fill(pygame.Color(71, 91, 141))
        self.color = pygame.Color(71, 91, 141)
        self.text_color = pygame.Color('black')
        self.text = text
        self.txt_surface = pygame.font.Font(None, 32).render(text, True, self.text_color)
        self.active = False

    def handle_event(self, event):
        res_event = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = pygame.Color('red') if self.active else pygame.Color(71, 91, 141)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if self.text:
                        res_event = make_request_pos(self.text)
                    else:
                        print('у вас пустое поле текста')
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.text_color)
        self.image.fill(self.color)
        self.image.blit(self.txt_surface, self.txt_surface.get_rect())
        return res_event



class Theme(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.add(theme_group)
        self.image = pygame.Surface((65, 35), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(525, 405, 65, 35)
        pygame.draw.rect(self.image, pygame.Color(71, 91, 141), (0, 0, 65, 35))
        font = pygame.font.Font(None, 30)
        text = font.render("Тема", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.rect.width / 2, self.rect.height / 2))
        self.image.blit(text, text_rect)


btn_theme = Theme(all_sprites)
map_im = make_request_map(z_const, coord, theme)
address_input = InputBox(50,0,500, 20, '')
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        ll_obj = address_input.handle_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                z_const = z_const + 1 if z_const != 21 else 21
            elif event.key == pygame.K_PAGEDOWN:
                z_const = z_const - 1 if z_const != 0 else 0
            elif event.key == pygame.K_RIGHT:
                coord[0] = str(float(coord[0]) + moving_long[z_const]) if float(coord[0]) + moving_long[
                    z_const] < 180.0 else str(-360 + float(coord[0]) + moving_long[z_const])
            elif event.key == pygame.K_LEFT:
                coord[0] = str(float(coord[0]) - moving_long[z_const]) if float(coord[0]) - moving_long[
                    z_const] > -180.0 else str(360 + float(coord[0]) - moving_long[z_const])
            elif event.key == pygame.K_UP:
                coord[1] = str(float(coord[1]) + moving_lat[z_const]) if float(coord[1]) + moving_lat[
                    z_const] < 85 else str(-170 + float(coord[1]) + moving_lat[z_const])
            elif event.key == pygame.K_DOWN:
                coord[1] = str(float(coord[1]) - moving_lat[z_const]) if float(coord[1]) - moving_lat[
                    z_const] > -85 else str(170 + float(coord[1]) - moving_lat[z_const])
            map_im = make_request_map(z_const, coord, theme, obj_ll=ll_obj)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn_theme.rect.collidepoint(pygame.mouse.get_pos()):
                print(1)
                if theme == 'dark':
                    theme = 'light'
                else:
                    theme = 'dark'
            map_im = make_request_map(z_const, coord, theme)
    screen.blit(map_im, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

os.remove('map.png')
pygame.quit()
