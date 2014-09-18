import sys
import RPi.GPIO as GPIO
import time

__author__ = 'Parker'

# light name, pin value
LIGHTS = {'red': 4, 'amber': 3, 'green': 2}
VERBOSE = True

ON = False
OFF = True


class Light:
    name = "undefined"
    status = False
    locked = False
    pin = 0

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
        print 'Locking %s light' % self.name
        self.locked = True

    def Unlock(self):
        print 'Unlocking %s light' % self.name
        self.locked = False

    def On(self):
        print 'Turning on %s light' % self.name
        self.status = ON
        self.Output()

    def Off(self):
        print 'Turning off %s light' % self.name
        self.status = OFF
        self.Output()

    def Toggle(self):
        print 'Toggling %s light' % self.name
        self.status = not self.status
        self.Output()

    def Output(self):
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
        GPIO.cleanup()

if __name__ == "__main__":
    main()
