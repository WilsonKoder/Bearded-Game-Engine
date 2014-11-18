__author__ = 'WilsonKoder'

import pygame
import pymunk
import pymunk.pygame_util
import pygame.gfxdraw

elasticity = 0.8
colours = {"red": (255, 0, 0), "blue": (0, 0, 255), "green": (0, 255, 0), "black": (0, 0, 0), "white": (255, 255, 255),
            "yellow": (255, 255, 0), "pink": (255, 0, 255), "cyan": (0, 255, 255), "purple": (135, 0, 255),
            "navy": (0, 90, 140)}

class bgeDraw:
    def draw_shapes(self, shapes):
        for shape in shapes:
            p_shape = int(shape.body.position.x), 600-int(shape.body.position.y)
            pygame.gfxdraw.filled_circle(screen, p_shape[0], p_shape[1], int(shape.radius), colours["red"])
            pygame.gfxdraw.aacircle(screen, p_shape[0], p_shape[1], int(shape.radius), colours["red"])
            #  the reason i drew a aa circle and a filled circle is to give the illusion of a smoothed filled circle.
            #  because if you just have the aacircle then its hollow, but if you just have the filled circle, it's
            #  got a lot of jaggies. bit performance heavy, but looks nice :)
    def draw_players(self, players):
        for player in players:
            p_player = int(player.body.position.x), 600-int(player.body.position.y)
            pygame.gfxdraw.filled_circle(screen, p_player[0], p_player[1], int(player.radius), colours["green"])
            pygame.gfxdraw.aacircle(screen, p_player[0], p_player[1], int(player.radius), colours["blue"])

class bgePhysics:
    def create_world(self, gravity):
        spc = pymunk.Space()
        spc.gravity = gravity
        return spc

    def add_player(self, radius, position):
        mass = 1
        inertia = pymunk.moment_for_circle(mass, 0, radius)
        body = pymunk.Body(mass, inertia)
        body.position = position
        player = pymunk.Circle(body, radius)
        player.elasticity = elasticity
        space.add(body, player)
        return player

    def add_circle(self, radius, position):
        mass = 1
        inertia = pymunk.moment_for_circle(mass, 0, radius)
        body = pymunk.Body(mass, inertia)
        body.position = position
        shape = pymunk.Circle(body, radius)
        shape.elasticity = elasticity
        space.add(body, shape)
        return shape

    def add_floor(self):
        body = pymunk.Body()
        body.position = (400, 500)
        line_shape = pymunk.Segment(body, (-400, -500), (400, -500), 15)
        line_shape.elasticity = 0.5
        space.add(line_shape)
        return line_shape

    def physics_move(self, direction, player):
        if direction == "right":
            #player.body.apply_force((player.body.position.x + 10, player.body.position.y))
            pass
        elif direction == "left":
            #player.body.apply_force((player.body.position.x + 10, player.body.position.y), (player.body.position.x + 10, player.body.position.y))
            pass





print("\nWelcome to Bearded Game Engine\n")

#width = int(input("Please input window width (pixels)"))
#height = int(input("Please input window height (pixles)"))

window_size = (800, 600)

pygame.init()

physics = bgePhysics()
draw = bgeDraw()

screen = pygame.display.set_mode(window_size)
space = physics.create_world((0.0, -900.0))

running = True

line = physics.add_floor()
line.color = colours["blue"]
shapes_list = []
player_list = []
colour = colours["red"]
clock = pygame.time.Clock()

edit_mode = True

#movement variables
move_left = False
move_right = False

while running:
    if edit_mode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    space.remove(shapes_list)
                    shapes_list = []
                if event.key == pygame.K_p:
                    edit_mode = False
                    print("entering playmode")
            elif event.type == pygame.KEYUP:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos() # get the mouse pos
                real_pos = pymunk.pygame_util.to_pygame(pos, screen)
                circle = physics.add_circle(14, real_pos)
                shapes_list.append(circle)
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    move_right = True
                elif event.key == pygame.K_a:
                    move_left = True
                elif event.key == pygame.K_SPACE:
                    pass
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    move_right = False
                elif event.key == pygame.K_a:
                    move_left = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos() # get the mouse pos
                real_pos = pymunk.pygame_util.to_pygame(pos, screen)
                player = physics.add_player(14, real_pos)
                player_list.append(player)


    if move_left:
        physics.physics_move("left", player_list[0])
    if move_right:
        physics.physics_move("right", player_list[0])

    screen.fill(colours["white"])

    ### ONLY DO DRAWING AFTER THIS LINE ###
    pymunk.pygame_util.draw(screen, line)
    draw.draw_shapes(shapes_list)
    draw.draw_players(player_list)

    space.step(1 / 60.0)
    clock.tick(60)

    pygame.display.flip()


