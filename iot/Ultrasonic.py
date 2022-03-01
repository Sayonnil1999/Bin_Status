import RPi.GPIO as GPIO
import time
import signal
import sys
from queue import Queue
import EditText

# use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
pinTrigger = 21
pinEcho = 20


def close(signal, frame):
    print("\nTurning off ultrasonic distance detection...\n")
    GPIO.cleanup()
    sys.exit(0)


signal.signal(signal.SIGINT, close)


class Ultrasonic:
    def __init__(self):
        self.dis = 0
        self.q = Queue(maxsize=EditText.max_que)
        self.sum = 0

    def ultrasonic_distance(self):
        # set GPIO input and output channels
        GPIO.setup(pinTrigger, GPIO.OUT)
        GPIO.setup(pinEcho, GPIO.IN)

        while True:
            # set Trigger to HIGH
            GPIO.output(pinTrigger, True)
            # set Trigger after 0.01ms to LOW
            time.sleep(0.00001)
            GPIO.output(pinTrigger, False)

            startTime = time.time()
            stopTime = time.time()

            # save start time
            while 0 == GPIO.input(pinEcho):
                startTime = time.time()

            # save time of arrival
            while 1 == GPIO.input(pinEcho):
                stopTime = time.time()

            # time difference between start and arrival
            TimeElapsed = stopTime - startTime
            # multiply with the sonic speed (34300 cm/s)
            # and divide by 2, because there and back
            distance = (TimeElapsed * 34300) / 2
            print("Distance: %.1f cm" % distance)
            if distance < EditText.avg_dist:
                if self.q.qsize() < self.q.maxsize:
                    self.q.put(distance)
                else:
                    self.sum -= self.q.get()
                    # self.q.get()
                    self.q.put(distance)
                self.sum += distance
            elif distance > EditText.avg_dist:
                if self.q.qsize() != 0:
                    self.q.get()
                else:
                    pass
            if self.q.qsize() == self.q.maxsize:
                self.avg = self.sum // self.q.qsize()
                # self.avg = sum(self.q.queue) // self.q.qsize()
                if self.avg < EditText.warn_limit:
                    print("Avg = ", self.avg)
                    EditText.notify.send()
                    GPIO.cleanup()
                    break
            time.sleep(1)
