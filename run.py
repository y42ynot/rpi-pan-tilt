# imports
#import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
#from RpiMotorLib import RpiMotorLib

from sshkeyboard import listen_keyboard

# variables
panpins = [1,2,3,4] # pin 1-4 on the stepper motor on pi
tiltpins = [1,2,3,4]
tiltlimitpin = 10
panlimitpin = 10
panpos = 0
tiltpos = 0
panlim = 1000
tiltlim = 1000


# functions
def pan(steps,direction): #true is clockwise false is counterclockwise                                   
    #RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ").motor_run(panpins,.001, steps, direction, False, "half", .05)
    print("pan equals "+str(panpos))

def tilt(steps,direction):
    #RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ").motor_run(tiltpins,.001, steps, direction, False, "half", .05)
    print("tilt equals "+str(tiltpos))

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
            panpos = panpos + steps
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
        if tiltpos - steps < 0:
            print("sorry, but that would push me past my limits. please try moving the other way")
            return False
        else:
            tiltpos = tiltpos - steps
            return True

 
# def init():
#     print("gimme a moment to set stuff up so you don't screw anything up")
    #GPIO.setwarnings(False) # Ignore warning for now #sets up limit switches
    #GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    #GPIO.setup(tiltlimitpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #GPIO.setwarnings(False) # Ignore warning for now #sets up limit switches
    #GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    #GPIO.setup(panlimitpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  


    #zero pan
    # while True:
    #     if GPIO.input(panlimitpin) == GPIO.HIGH:
    #         pan(1,True) 

    #     else:
    #         break
    # #zero tilt
    # while True:
    #     if GPIO.input(tiltlimitpin) == GPIO.HIGH:
    #         tilt(1,True) 


# logs keystrokes assigns roles to them
def press(key):
    if key == "up":
        if checktilt(20,True):
            tilt(20,True)

    elif key == "down":
        if checktilt(20,False):
            tilt(20,False)
 
        print("")
    elif key == "left":
        if checkpan(20,True):
            pan(20,True)

    elif key == "right":
        if checkpan(20,False):
            pan(20,False)

    elif key == "w":
        if checktilt(1,True):
            tilt(1,True)
 
    elif key == "s":
        if checktilt(1,False):
            tilt(1,False)

    elif key == "a":
        if checkpan(1,True):
            pan(1,True)

    elif key == "d":
        if checkpan(1,False):
            pan(1,False)
        


#code
#init()
listen_keyboard(on_press=press)




