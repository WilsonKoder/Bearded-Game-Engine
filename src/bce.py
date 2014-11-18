__author__ = 'WilsonKoder'

import pygame
import pymunk
import pymunk.pygame_util
import pygame.gfxdraw

elasticity = 0.8
colours = {"red": (255, 0, 0), "blue": (0, 255, 0), "green": (0, 0, 255), "black": (0, 0, 0), "white": (255, 255, 255),
            "yellow": (255, 255, 0), "pink": (255, 0, 255), "cyan": (0, 255, 255), "purple": (135, 0, 255),
            "navy": (0, 90, 140)}

class bceDraw:
    def draw_shapes(self, shapes):
        for shape in shapes:
            p_shape = int(shape.body.position.x), 600-int(shape.body.position.y)
            pygame.gfxdraw.filled_circle(screen, p_shape[0], p_shape[1], int(shape.radius), colours["red"])
            pygame.gfxdraw.aacircle(screen, p_shape[0], p_shape[1], int(shape.radius), colours["red"])
            #  the reason i drew a aa circle and a filled circle is to give the illusion of a smoothed filled circle.
            #  because if you just have the aacircle then its hollow, but if you just have the filled circle, it's
            #  got a lot of jaggies. bit performance heavy, but looks nice :)

class bcePhysics:
    def create_world(self, gravity):
        spc = pymunk.Space()
        spc.gravity = gravity
        return spc
    def add_circle(self, radius, position):
        mass = 1
        inertia = pymunk.moment_for_circle(mass, 0, radius)
        body = pymunk.Body(mass, inertia)
        body.position = position
        shape = pymunk.Circle(body, radius)
        shape.elasticity = elasticity
        space.add(body, shape)
        return shape


print("\nWelcome to Bearded Computing Engine\n")

width = int(input("Please input window width (pixels)"))
height = int(input("Please input window height (pixles)"))

window_size = (width, height)

pygame.init()

physics = bcePhysics()
draw = bceDraw()

screen = pygame.display.set_mode(window_size)
space = physics.create_world((0.0, -900.0))

running = True

shapes_list = []
colour = colours["red"]
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            pass
        elif event.type == pygame.KEYUP:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos() # get the mouse pos
            real_pos = pymunk.pygame_util.to_pygame(pos, screen)
            circle = physics.add_circle(14, real_pos)
            shapes_list.append(circle)

    screen.fill(colours["white"])

    ### ONLY DO DRAWING AFTER THIS LINE ###
    draw.draw_shapes(shapes_list)

    space.step(1 / 60.0)
    clock.tick(60)

    pygame.display.flip()


