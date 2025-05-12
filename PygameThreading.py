import pygame, cv2, math, time, numpy, threading
from djitellopy import Tello

pygame.init()
pygame.display.set_caption("Tello video stream")

tello = Tello()
tello.connect()
tello.streamon()
tello.set_speed(100)

screen = pygame.display.set_mode((960, 720))
FPS = 120
pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // FPS)

run = True
is_takeoff_land = False
#def displayImageLoop(run):
 #   while run == True:
 #       img = frame_read.frame
 #       img = numpy.rot90(img)
 #       img = numpy.flipud(img)
 #       sf = pygame.surfarray.make_surface(img)
 #       screen.blit(sf, (0, 0))
 #       pygame.display.flip()

#old
def checkKeys():
    global run
    lr_velocity = 0 #left = - | right   = +
    fb_velocity = 0 #back = - | forward = +
    ud_velocity = 0 #down = - | up      = +
    yaw         = 0 #left = - | right   = +
    keyRun = True
    while run:
        continue
        if tello.is_flying:
            keyRun = False
        #tello.send_rc_control(lr_velocity, fb_velocity, ud_velocity, yaw)
        
        pressed = pygame.key.get_pressed()
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
            run = False
        if pressed[pygame.K_o] == True:
            tello.takeoff()
        if pressed[pygame.K_j] and pressed[pygame.K_BACKSLASH]:
            tello.emergency()
#old
def displayImage():
    global run
    while run:
        img = frame_read.frame
        img = numpy.rot90(img)
        img = numpy.flipud(img)
        sf = pygame.surfarray.make_surface(img)
        screen.blit(sf, (0, 0))
#old
def eventHandle():
    global run
    for event in pygame.event.get():
            pass
            if event.type == pygame.QUIT:
                run = False

lr_velocity = 0
fb_velocity = 0
ud_velocity = 0
yaw         = 0 
lr_velocity_old = 0 
fb_velocity_old = 0 
ud_velocity_old = 0 
yaw_old         = 0  
invalid_keys = 0
thread1 = threading.Thread

def handleKeyPress(event):
    global lr_velocity 
    global fb_velocity 
    global ud_velocity
    global yaw
    global invalid_keys
    
    key = event.key

    # Default the direction to keys being pressed
    direction = 1
    
    # If the key is being released, reverse the normal direction
    if event.type == pygame.KEYUP:
        direction = -1
    if tello.is_flying and invalid_keys <= 0: # and thread1.is_alive() == False:
        match key:
            case pygame.K_w:
                fb_velocity += 50*direction
            case pygame.K_s:
                fb_velocity -= 50*direction
            case pygame.K_d:
                lr_velocity  +=50*direction
            case pygame.K_a:
                lr_velocity -=50*direction
            case pygame.K_q:
                yaw -= 50*direction
            case pygame.K_e:
                yaw +=50*direction
            case pygame.K_z:
                ud_velocity +=50*direction
            case pygame.K_x:
                ud_velocity -=50*direction
            case pygame.K_y :
                if event.type == pygame.KEYDOWN:
                    thread2 = createThread('flip')
                    thread2.start()
            case pygame.K_ESCAPE:
                if event.type == pygame.KEYDOWN:
                    lr_velocity = fb_velocity = yaw = ud_velocity = 0
                    thread1 = createThread('land')
                    thread1.start()
        tello.send_rc_control(lr_velocity, fb_velocity, ud_velocity, yaw)

    elif (tello.is_flying != True or invalid_keys >0) and event.type == pygame.KEYDOWN and key != pygame.K_o:
        invalid_keys += 1
        print(invalid_keys)
    elif invalid_keys > 0 and event.type == pygame.KEYUP and key != pygame.K_o:
        invalid_keys -= 1
        print(invalid_keys)
    
    elif event.type == pygame.KEYDOWN and key == pygame.K_o:
        thread1 = createThread('takeoff')
        thread1.start()

def sendTelloSpeed():
    global lr_velocity_old #left = - | right   = +
    global fb_velocity_old 
    global ud_velocity_old #down = - | up      = +
    global yaw_old         #ft = - | right   = +
    global lr_velocity #left = - | right   = +
    global fb_velocity 
    global ud_velocity #down = - | up      = +
    global yaw         #ft = - | right   = +
    if lr_velocity_old != lr_velocity or fb_velocity_old != fb_velocity or ud_velocity_old != ud_velocity or yaw_old != yaw:
        tello.send_rc_control(lr_velocity, fb_velocity, ud_velocity, yaw)
        lr_velocity_old = lr_velocity
        fb_velocity_old = fb_velocity
        ud_velocity_old = ud_velocity
        yaw_old = yaw

def createThread(takeoff_or_land):
    return threading.Thread(target=takeoffLand, args=(takeoff_or_land,))

def takeoffLand(cmd):
    #global is_takeoff_land
    #is_takeoff_land = True
    if cmd == 'takeoff':
        tello.takeoff()
    elif cmd == 'land':
        tello.is_flying = False
        tello.land()
    elif cmd == 'flip':
        tello.flip_forward()
    #is_takeoff_land = False
    return
        

tello.streamoff()
tello.streamon()
frame_read = tello.get_frame_read(with_queue= False)

while run:

    #sf = pygame.surfarray.make_surface(img)
    
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                handleKeyPress(event)
            
    #sendTelloSpeed()
    screen.fill([0, 0, 0])

    img = frame_read.frame
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = numpy.rot90(img)
    img = numpy.flipud(img)
    sf = pygame.surfarray.make_surface(img)
    screen.blit(sf, (0, 0))
    pygame.display.update()
    time.sleep(1/FPS)

if tello.is_flying:
    tello.land() 