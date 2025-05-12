import pygame, cv2, math, time, numpy, threading, queue, pygame.freetype
from djitellopy import Tello

pygame.init()
pygame.display.set_caption("Tello video stream")
#text = pygame.font.Font('ariel',30)

tello = Tello()
tello.connect()
tello.streamon()
tello.set_speed(100)
screen = pygame.display.set_mode((960, 720))
FPS = 120
pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // FPS)
pygame.freetype.init()
#text_font = pygame.freetype.Font('arial' ,30)
old_text = None
run = True

lr_velocity     = 0
fb_velocity     = 0
ud_velocity     = 0
yaw             = 0 
lr_velocity_old = 0 
fb_velocity_old = 0
ud_velocity_old = 0 
yaw_old         = 0  
invalid_keys    = 0
commandthread = threading.Thread

main_to_command = queue.Queue()
command_to_main = queue.Queue()

keys_blocked = False

#def updateText(battery):
    #battery_text = text.render(battery, 0,0)
    #screen.blit(battery_text,0,0)

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
     # and thread1.is_alive() == False:
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
        case pygame.K_t:
            if event.type == pygame.KEYDOWN:
                sendCommand('flip forward')

        case pygame.K_DELETE:
            tello.emergency()
            tello.is_flying = False
        case pygame.K_ESCAPE:
            if event.type == pygame.KEYDOWN:
                sendCommand('land')
        case pygame.K_o:
            if event.type == pygame.KEYDOWN and not tello.is_flying:
                sendCommand('takeoff')

def sendCommand(cmd):
    print("Existing command: ", yaw)
    global keys_blocked
    if not keys_blocked:
        main_to_command.put(cmd)
        keys_blocked = True


def commandThread():
    active = True
    while active:
        command = main_to_command.get()
        match command:
            case 'takeoff':
                tello.takeoff()
                
            case 'land':
                tello.land()
                
            case 'quit':
                return
            case 'flip forward':
                tello.flip('forward')
        command_to_main.put('done')

def sendTelloSpeed(force):
    global lr_velocity_old 
    global fb_velocity_old 
    global ud_velocity_old 
    global yaw_old         
    global lr_velocity
    global fb_velocity 
    global ud_velocity
    global yaw
    if not tello.is_flying:
        return         
    if lr_velocity_old != lr_velocity or fb_velocity_old != fb_velocity or ud_velocity_old != ud_velocity or yaw_old != yaw or force:
        tello.send_rc_control(lr_velocity, fb_velocity, ud_velocity, yaw)
        lr_velocity_old = lr_velocity
        fb_velocity_old = fb_velocity
        ud_velocity_old = ud_velocity
        yaw_old = yaw

def takeoffLand(cmd):
    match cmd:
        case 'takeoff':
            tello.takeoff()
        case 'land':
            tello.is_flying = False
            tello.land()
        case'flip':
            tello.flip_forward()
    #is_takeoff_land = False
    return
     
def updateText(text, surface):
    global old_text
    if text != old_text:
        old_text = text
        text_font.render_to(surface, (100, 100), text, (255, 255, 255))
        screen.blit(surface,(0,0))
frame_read = tello.get_frame_read(with_queue= False)

surface = pygame.Surface((960,720))


command = threading.Thread(target=commandThread)
command.start()
while run:

    #sf = pygame.surfarray.make_surface(img)
    
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sendCommand('quit')
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                handleKeyPress(event)

    try:
        if command_to_main.get(False) != None:
            print("Finished command")
            print("Value after command: ", yaw)
            keys_blocked = False
            sendTelloSpeed(True)
    except Exception:
        pass
    finally:
        pass

    #updateText(str(tello.get_battery()))
    
    if not keys_blocked:
        sendTelloSpeed(False)
    
    screen.fill([0, 0, 0])
    img = frame_read.frame
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = numpy.rot90(img)
    img = numpy.flipud(img)
    sf = pygame.surfarray.make_surface(img)
    screen.blit(sf, (0, 0))
    pygame.display.update()
    #updateText(tello.get_battery,surface)
    time.sleep(1/FPS)

if tello.is_flying:
    tello.land() 
command.join()