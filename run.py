# imports
#import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
#from RpiMotorLib import RpiMotorLib
import curses



# variables
panpins = [8,10,12,16] # pin 1-4 on the stepper motor on pi
tiltpins = [7,11,13,15]
tiltlimitpin = 21
panlimitpin = 19
panpos = 0
tiltpos = 0
panlim = 11410
tiltlim = 12190

# get the curses screen window
screen = curses.initscr()
def draw(string,height):
    screen.addstr(height,0,string)  # overwrite the old stuff with spaces
    screen.clrtoeol()
    screen.refresh()
# turn off input echoing
curses.noecho()

# respond to keys immediately (don't wait for enter)
curses.cbreak()

# map arrow keys to special values
screen.keypad(True)

# functions
def pan(steps,direction): #true is clockwise false is counterclockwise                                   
    #RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ").motor_run(panpins,.001, steps, direction, False, "half", .05)
    draw("pan is "+str(round((panpos/panlim)*180,1))+" degrees",1)

def tilt(steps,direction):
    #RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ").motor_run(tiltpins,.001, steps, direction, False, "half", .05)
    draw("tilt is "+str(round((tiltpos/tiltlim)*180,1))+" degrees",2)


def checkpan(steps,direction):
    global panpos
    if direction:
        if panpos + steps > panlim:
            draw("sorry, but that would push me past my limits. please try moving the other way",1)
            return False
        else:
            panpos = panpos + steps
            return True
    else:
        if panpos - steps < 0:
            draw("sorry, but that would push me past my limits. please try moving the other way",1)
            return False
        else:
            panpos = panpos - steps
            return True
def checktilt(steps,direction):
    global tiltpos
    if direction:
        if tiltpos + steps > tiltlim:
            draw("sorry, but that would push me past my limits. please try moving the other way",2)
            return False
        else:
            tiltpos = tiltpos + steps
            return True
    else:
        if tiltpos - steps < 10:
            draw("sorry, but that would push me past my limits. please try moving the other way",2)
            return False
        else:
            tiltpos = tiltpos - steps
            return True

def init():
    global panpos
    global tiltpos
    print("gimme a moment to set stuff up so you don't screw anything up")
    GPIO.setwarnings(False) # Ignore warning for now #sets up limit switches
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(tiltlimitpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setwarnings(False) # Ignore warning for now #sets up limit switches
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(panlimitpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  


    #zero pan
    while True:
        if GPIO.input(panlimitpin) == GPIO.HIGH: 
            panpos = 5978
            break
        else:
            pan(1,True)
    #zero tilt
    while True:
        if GPIO.input(tiltlimitpin) == GPIO.HIGH:
            tilt(600,False)
            tiltpos = 0
            break
        else:
            tilt(1,True) 


# # logs keystrokes assigns roles to them
# def press(key):
#     if key == "up":
#         if checktilt(500,True):
#             tilt(500,True)

#     elif key == "down":
#         if checktilt(500,False):
#             tilt(500,False)
 
#         print("")
#     elif key == "left":
#         if checkpan(500,True):
#             pan(500,True)

#     elif key == "right":
#         if checkpan(500,False):
#             pan(500,False)

#     elif key == "w":
#         if checktilt(100,True):
#             tilt(100,True)
 
#     elif key == "s":
#         if checktilt(100,False):
#             tilt(100,False)

#     elif key == "a":
#         if checkpan(100,True):
#             pan(100,True)

#     elif key == "d":
#         if checkpan(100,False):
#             pan(100,False)

# def end():
#     if panpos < 5000:
#         pan(5000-panpos,True)
#     else:
#         pan(panpos-5000,False)
        


#code
#init()

#end()




try:
    while True:
        char = screen.getch()
        if char == ord('q'):
            break
        elif char == curses.KEY_RIGHT:
           if checkpan(500,True):
                pan(500,True)
        elif char == curses.KEY_LEFT:
             if checkpan(500,False):
                pan(500,False)
        elif char == curses.KEY_UP:
            if checktilt(500,True):
                tilt(500,True)
        elif char == curses.KEY_DOWN:
            if checktilt(500,False):
                tilt(500,False)
finally:
    # shut down cleanly
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()


