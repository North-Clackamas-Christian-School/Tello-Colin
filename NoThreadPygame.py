import pygame, cv2, math, time, numpy, threading
from djitellopy import Tello

pygame.init() 

tello = Tello()
tello.connect()
tello.streamon()
tello.set_speed(100)

frame_read = tello.get_frame_read(with_queue= False)

screen = pygame.display.set_mode((1000, 600))


lr_velocity = 0 #left = - | right   = +
fb_velocity = 0 #back = - | forward = +
ud_velocity = 0 #down = - | up      = +
yaw         = 0 #left = - | right   = +


run = True
while run:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #if event.type == pygame.KEYDOWN:
                #print(pygame.key.name(event.key))

    img = frame_read.frame
    img = numpy.rot90(img)
    img = numpy.flipud(img)
    sf = pygame.surfarray.make_surface(img)
    screen.blit(sf, (0, 0))
    pygame.display.flip()

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_o] == True:
            tello.takeoff()
    
    tello.send_rc_control(lr_velocity, fb_velocity, ud_velocity, yaw)
    if pressed[pygame.K_w]:
        fb_velocity = 50
    elif pressed[pygame.K_s]:
        fb_velocity = -50
    elif pressed[pygame.K_w] == False and pressed[pygame.K_s] == False:
        fb_velocity = 0
    
    if pressed[pygame.K_a]:
        lr_velocity = -50
    elif pressed[pygame.K_d]:
        lr_velocity = 50
    elif pressed[pygame.K_a] == False and pressed[pygame.K_d] == False:
        lr_velocity = 0

    if pressed[pygame.K_z]:
        ud_velocity = 50
    elif pressed[pygame.K_x]:
        ud_velocity = -50
    elif pressed[pygame.K_x] == False and pressed[pygame.K_z] == False:
        ud_velocity = 0

    if pressed[pygame.K_q]:
        yaw = -50
    elif pressed[pygame.K_e]:
        yaw = 50
    elif pressed[pygame.K_q] == False and pressed[pygame.K_e] == False:
        yaw = 0

    if pressed[pygame.K_j] and [pygame.K_u]:
        tello.flip_forward()
    if pressed[pygame.K_j] and [pygame.K_h]:
        tello.flip_left()
    if pressed[pygame.K_j] and [pygame.K_k]:
        tello.flip_right()

    if pressed[pygame.K_ESCAPE] == True:
        #run = False
        tello.land()
    if pressed[pygame.K_j] and pressed[pygame.K_BACKSLASH]:
        tello.emergency()