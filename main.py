import sys
import RPi.GPIO as GPIO
import time

# light name, pin value
LIGHTS = {'red': 4, 'amber': 3, 'green': 2}
VERBOSE = True  # TODO use better logging

# simply to resolve any confusion
ON = False
OFF = True


class Light:
    name = "undefined"  # human-friendly name of the light
    status = False  # light status
    locked = False  # lock status
    pin = 0  # GPIO pin

    def __init__(self, name, pin):
        print 'Setting up %s light (pin %s)' % (name, pin)
        self.pin = pin
        self.name = name

        GPIO.setup(self.pin, GPIO.OUT)

        # quick bulb test
        self.On()
        time.sleep(0.25)
        self.Off()
        time.sleep(0.25)

    def Lock(self):
        """Locks a light to its current status"""
        print 'Locking %s light' % self.name
        self.locked = True

    def Unlock(self):
        """Unlocks the light, allowing for it to change"""
        print 'Unlocking %s light' % self.name
        self.locked = False

    def On(self):
        """Sends a command to the relay to complete the circuit for the lamp"""
        print 'Turning on %s light' % self.name
        self.status = ON
        self.Output()

    def Off(self):
        """Sends a command to the relay to cut the circuit for the lamp"""
        print 'Turning off %s light' % self.name
        self.status = OFF
        self.Output()

    def Toggle(self):
        """Sends a command to the relay  to be the opposite of
        whatever it is"""
        print 'Toggling %s light' % self.name
        self.status = not self.status
        self.Output()

    def Output(self):
        """Actually sends the command to the relay
        This is where the locked flag is checked"""
        if not self.locked:
            if VERBOSE:
                print '%s light status: %s' % (self.name, self.status)
            GPIO.output(self.pin, self.status)
        else:
            if VERBOSE:
                print '%s light is locked' % (self.name)


def main():
    try:
        print 'Setting GPIO mode...'
        GPIO.setmode(GPIO.BCM)

        # populate the light dictionary
        lights = {}
        for light_name in LIGHTS.keys():
            lights[light_name] = Light(light_name, LIGHTS[light_name])

        lights['red'].On()
        lights['red'].Lock()

        while True:
            for light in lights:
                time.sleep(1)
                lights[light].Toggle()

    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

    finally:
        # if you don't clean up you're gonna have a bad time
        GPIO.cleanup()

if __name__ == "__main__":
    main()
