# imports
#import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
#from RpiMotorLib import RpiMotorLib
from sshkeyboard import listen_keyboard



# variables
panpins = [14,15,18,23] # pin 1-4 on the stepper motor on pi
tiltpins = [4,17,27,22]
tiltlimitpin = 9
panlimitpin = 10
panpos = 0
tiltpos = 0
panlim = 11410
tiltlim = 12190

# functions
def pan(steps,direction): #true is clockwise false is counterclockwise                                   
    #RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ").motor_run(panpins,.001, steps, direction, False, "half", .05)
    print("pan is "+str(round((panpos/panlim)*180,1))+" degrees")

def tilt(steps,direction):
    #RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ").motor_run(tiltpins,.001, steps, direction, False, "half", .05)
    print("tilt is "+str(round((tiltpos/tiltlim)*180,1))+" degrees")


def checkpan(steps,direction):
    global panpos
    if direction:
        if panpos + steps > panlim:
            print("sorry, but that would push me past my limits. please try moving the other way")
            return False
        else:
            panpos = panpos + steps
            return True
    else:
        if panpos - steps < 0:
            print("sorry, but that would push me past my limits. please try moving the other way")
            return False
        else:
            panpos = panpos - steps
            return True
def checktilt(steps,direction):
    global tiltpos
    if direction:
        if tiltpos + steps > tiltlim:
            print("sorry, but that would push me past my limits. please try moving the other way")
            return False
        else:
            tiltpos = tiltpos + steps
            return True
    else:
        if tiltpos - steps < 10:
            print("sorry, but that would push me past my limits. please try moving the other way")
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


# logs keystrokes assigns roles to them
def press(key):
    if key == "up":
        if checktilt(500,True):
            tilt(500,True)
    elif key == "down":
        if checktilt(500,False):
            tilt(500,False)
        print("")
    elif key == "left":
        if checkpan(500,True):
            pan(500,True)
    elif key == "right":
        if checkpan(500,False):
            pan(500,False)
    elif key == "w":
        if checktilt(100,True):
            tilt(100,True)
    elif key == "s":
        if checktilt(100,False):
            tilt(100,False)
    elif key == "a":
        if checkpan(100,True):
            pan(100,True)
    elif key == "d":
        if checkpan(100,False):
            pan(100,False)

def end():
    if panpos < 5000:
        pan(5000-panpos,True)
    else:
        pan(panpos-5000,False)
        


#code
#init()
listen_keyboard(on_press=press)
#end()



