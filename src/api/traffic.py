from flask import Flask, jsonify
import sys
import RPi.GPIO as GPIO
import time
import operator
app = Flask(__name__)

__author__ = 'Parker'

lights = {}

@app.route('/light/<name>', methods=['POST'])
def toggle(name):
    lights[name].Toggle()
    return str(lights[name].status)

@app.route('/light/<name>/on', methods=['POST'])
def on(name):
    lights[name].On()
    return str(lights[name].status)

@app.route('/light/<name>/off', methods=['POST'])
def off(name):
    lights[name].Off()
    return str(lights[name].status)

@app.route('/light/<name>', methods=['GET'])
def status(name):
    return jsonify(light=name, status=lights[name].status)

# light name, pin value
LIGHTS = { 'red': 2, 'amber': 4, 'green': 3 }
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

    def Flash(self):
        print 'Flashing %s light' % self.name
        self.Off()
        self.On()
        time.sleep(0.5)
        self.Off()

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
        sortedLights = sorted(LIGHTS.items(), key=operator.itemgetter(1), reverse=False);

        for light in sortedLights:
            lights[light[0]] = Light(light[0], light[1])

    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

if __name__ == "__main__":
    try:
        GPIO.setmode(GPIO.BCM)
        main()
        app.run(host='0.0.0.0')
    finally:
        GPIO.cleanup()
~
~
~
~

