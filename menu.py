import pygame
import json
import collections
import os

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
done = False



_image_library = {}

def create_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
            image = pygame.image.load(path)
            _image_library[path] = image

def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
            image = pygame.image.load(path)
            _image_library[path] = image
    return image

def draw_image(image, x, y):
    screen.blit(image, (x, y))



#font = pygame.font.SysFont("comicsansms", 72)
#text = font.render("Hello, World", True, (0, 128, 0))
size = 20
font = pygame.font.Font(None, size)
_text_library = {}

def creat_text(text, color):
    global _text_library
    color = (0, 128, 0)
    _text_library[text] = font.render(text, True, color)

def get_text(text):
    global _text_library
    color = (0, 128, 0)
    s = _text_library.get(text)
    if s == None:
        s = font.render(text, True, color)
        _text_library[text] = s
    return s

def draw_text(text, x, y):
    screen.blit(text, (x, y))

def draw_text_centered(text, x, y):
    screen.blit(text,
        (x - text.get_width() // 2, y - text.get_height() // 2))

def draw_rect(x, y, width, height, color):
    pygame.draw.rect(screen, color, pygame.Rect(x, y, width, height))

_games = collections.OrderedDict()
_DATA_I = 0
_X_I = 1
_Y_I = 2

_Y_TOP = 60
_DELTA_Y = 50
def load():
    global _games
    global _DATA_I
    global _X_I 
    global _Y_I 

    global _Y_TOP
    global _DELTA_Y

    f = open('./games.json')
    s = f.read()
    f.close()
    j = json.loads(s)

    x = 100
    y = _Y_TOP
    y_space = _DELTA_Y
    for game in j['games']:
        _games[game['Name']] = [game, x, y]
        y += y_space

    #Jet Pac is used as a generic key. The key used does not matter as long as it has all the fields to be displayed
    lables = _games['Jet Pac'][_DATA_I].keys()
    for text in lables:
        creat_text(text + ': ', None)

    print 'debug:'
    print _games
    for game in _games:
        print '\t' + game
        for dict_key in _games[game][_DATA_I].keys():
            print '\t\t' + dict_key + ': ' + _games[game][_DATA_I][dict_key]
            creat_text(_games[game][_DATA_I][dict_key], None)
                
    
    print _games['Jet Pac'][_DATA_I]['Name']
    print _text_library.keys()
    create_image('./games/JetPac/JetPac.png')
    #end load

RECT_Y_TOP = 40
#RECT_Y_BOT = 120
rect_x = 10
rect_y = RECT_Y_TOP
rect_width = 200
rect_height = 40
color = (50, 50, 50)
load()
selected = _games.items()[0]
print '\n\n', selected
selected_i = 0
selected_data = _games.items()[selected_i][1][0]
print '\n', selected_data
while not done:
    #input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True

    pressed = pygame.key.get_pressed()
    #up
    if pressed[pygame.K_UP]: 
        if not rect_y <= RECT_Y_TOP: 
            rect_y -= _DELTA_Y
            selected_i -= 1
            selected_data = _games.items()[selected_i][1][0]
        elif selected_i != 0:
            selected_i -= 1
            selected_data = _games.items()[selected_i][1][0]
            for game in _games:
                print game
                _games[game][_Y_I] -= _DELTA_Y
    #down buggy
    if pressed[pygame.K_DOWN]:
        #if not rect_y >= RECT_Y_BOT:
        if selected_i != len(_games.items())-1:
            rect_y += _DELTA_Y
            selected_i += 1
            selected_data = _games.items()[selected_i][1][0]
        #elif selected_i != len(_games.items())-1:
         #   selected_i += 1
          #  selected_data = _games.items()[selected_i][1][0]
           # for game in _games:
            #    _games[game][_Y_I] += _DELTA_Y
    #enter
    if pressed[pygame.K_RETURN]:
        print selected_data['exe']
        os.popen(selected_data['exe'])
    
    #begin draw
    screen.fill((0, 0, 0))
    #cursor
    draw_rect(rect_x, rect_y, rect_width, rect_height, color)
    #list games
    for game_name in _games:
        #if _games[game_name][_Y_I] >= _Y_TOP and _games[game_name][_Y_I] < RECT_Y_BOT:
            draw_text_centered(_text_library[game_name], _games[game_name][_X_I], _games[game_name][_Y_I])
    #list selected details
    x = 400
    y = 50
    ydif = 40

    draw_text(get_text('Name: ' + selected_data['Name']), x, y)
    y += ydif
    draw_text(get_text('Developer: ' + selected_data['Developer']), x, y)
    y += ydif
    draw_text(get_text('Publisher: ' + selected_data['Publisher']), x, y)
    y += ydif
    draw_text(get_text('Year: ' + selected_data['Year']), x, y)
    y += ydif
    draw_text(get_text('System: ' + selected_data['System']), x, y)
    y += ydif
    draw_text(get_text('Genre: ' + selected_data['Genre']), x, y)
    y += ydif
    draw_text(get_text('Players: ' + selected_data['Players']), x, y)
    y += ydif
    draw_text(get_text('Screenshot: '), x, y)
    y += ydif
    draw_image(get_image(selected_data['Screenshot']), x, y)
    
    #draw_image(_image_library['./games/JetPac/JetPac.png'], 20, 20)
    
    
    
    
    pygame.display.flip()
    #fps
    clock.tick(15)