from djitellopy import Tello
import cv2, math, time

tello = Tello()
tello.connect()

tello.streamon()
frame_read = tello.get_frame_read()
tello.set_speed(100)
tello.takeoff()

lr_velocity = 0 #left = - | right   = +
fb_velocity = 0 #back = - | forward = +
ud_velocity = 0 #down = - | up      = +
yaw         = 0 #left = - | right   = +

while True:
    tello.send_rc_control(lr_velocity, fb_velocity, ud_velocity, yaw)
    img = frame_read.frame
    cv2.imshow("drone", img)
    key = cv2.waitKey(1) & 0xff
               
    if key == 27: #ESC
        break
    elif key == ord('w'):
        fb_velocity = 30
    elif key == ord('s'):
        fb_velocity = -30
    elif key == ord('a'):
        lr_velocity = -30
    elif key == ord('d'):
        lr_velocity = 30
    elif key == ord('e'):
        yaw = 30
    elif key == ord('q'):
        yaw = -30
    elif key == ord('r'):
        ud_velocity = -10
    elif key == ord('f'):
        ud_velocity = 10
    elif key == ord('o'):
        tello.flip_forward()
    elif key == ord('j'):
        tello.emergency()
    elif key == '-1':
        lr_velocity=0
        ud_velocity=0
        fb_velocity =0
        yaw = 0
    elif key == ord('l'):
        lr_velocity=0
        ud_velocity=0
        fb_velocity =0
        yaw = 0
tello.land()
