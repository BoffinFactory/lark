#!/usr/bin/python
import json
import os
import sys

import pygame


# Holds references to image objects
class Library:

    def __init__(self, font):
        self.image_library = {}
        self.text_library = {}
        self.font = font

    # returns the image found at the path given and creates a reference to it if needed
    def get_image(self, path):
        image = self.image_library.get(path)
        if image is None:
            try:
                image = pygame.image.load(path)
            except pygame.error:
                print 'image ' + path + ' not found'
                image = self.get_text(path, (255, 0, 0))
            self.image_library[path] = image
        return image

    # returns a text object
    def get_text(self, strs, color=(0, 128, 0)):
        text = self.text_library.get((strs, color))
        if text is None:
            text = self.font.render(strs, True, color)
            self.text_library[(strs, color)] = text
        return text


class Drawer:
    def __init__(self, screen):
        self.screen = screen

    def draw_text(self, text, x, y):
        self.screen.blit(text, (x, y))

    def draw_text_centered(self, text, x, y):
            self.screen.blit(text, (
                x - text.get_width() // 2, y - text.get_height() // 2))

    def draw_image(self, image, x, y):
        self.screen.blit(image, (x, y))

    def draw_rect(self, x, y, width, height, color=(50, 50, 50)):
        pygame.draw.rect(self.screen, color, pygame.Rect(x, y, width, height))


def load(path, games, images):
    with open(path) as fh:
        raw_str = fh.read()
    json_data = json.loads(raw_str)
    for game in json_data['games']:
        games.append(game)
        images.get_image(game['Screenshot'])
        print game
    print games


def gui(path):
    # Load
    # Pygame stuff
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600))
    # 'Game' loop condition
    done = False
    # Font name, size. Default is used
    font = pygame.font.Font(None, 20)
    d = Drawer(screen)
    lib = Library(font)
    games = []
    sorted_state = 'not sorted'
    load(path, games, lib)
    rect_y_top = 40
    rect_y_bot = 560
    rect_x = 10
    rect_y = rect_y_top
    rect_width = 200
    rect_height = 40
    delta_y = 50
    selected_game_i = 0
    top_of_screen_i = 0
    # 'Game' loop
    while not done:
        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = True

        pressed = pygame.key.get_pressed()
        # Up
        if pressed[pygame.K_UP]:
            if not rect_y <= rect_y_top:
                rect_y -= delta_y
                selected_game_i -= 1
            elif selected_game_i != 0:
                selected_game_i -= 1
                top_of_screen_i -= 1
        # Down
        if pressed[pygame.K_DOWN]:
            if not rect_y >= rect_y_bot - delta_y:
                rect_y += delta_y
                selected_game_i += 1
            elif selected_game_i != len(games) - 1:
                selected_game_i += 1
                top_of_screen_i += 1
        # Main Enter/return
        if pressed[pygame.K_RETURN]:
            exe = games[selected_game_i]['exe']
            print exe
            os.popen(exe)

        # Draw
        # Clear screen
        screen.fill((0, 0, 0))
        # cursor
        d.draw_rect(rect_x, rect_y, rect_width, rect_height)
        # Draw list of games
        x = 100
        y = 60
        for i in xrange(top_of_screen_i, len(games)):
            game = games[i]
            d.draw_text_centered(lib.get_text(game['Name']), x, y)
            y += delta_y

        x = 400
        y = 50
        ydif = 40
        game = games[selected_game_i]

        d.draw_text(lib.get_text('Name: ' + game['Name']), x, y)
        y += ydif
        d.draw_text(lib.get_text('Developer: ' + game['Developer']), x, y)
        y += ydif
        d.draw_text(lib.get_text('Publisher: ' + game['Publisher']), x, y)
        y += ydif
        d.draw_text(lib.get_text('Year: ' + game['Year']), x, y)
        y += ydif
        d.draw_text(lib.get_text('System: ' + game['System']), x, y)
        y += ydif
        d.draw_text(lib.get_text('Genre: ' + game['Genre']), x, y)
        y += ydif
        d.draw_text(lib.get_text('Players: ' + game['Players']), x, y)
        y += ydif
        d.draw_text(lib.get_text('Screenshot: '), x, y)
        y += ydif
        d.draw_image(lib.get_image(game['Screenshot']), x, y)
        y += ydif

        # Updates screen
        pygame.display.flip()
        # fps
        clock.tick(15)
        # End gui


def main():
    # Optional Hardcoded path
    default_config_path = None

    # cmd params
    if len(sys.argv) > 1:
        path = sys.argv[1]
    elif default_config_path is not None:
        path = default_config_path
    else:
        print 'Please provide a game list. See readme for details'
        sys.exit(1)
    print 'Loading from ', path

    gui(path)

if __name__ == '__main__':
    main()
