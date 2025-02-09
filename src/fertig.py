import multiprocessing as mp
import board
import neopixel
import time
import mss
import numpy as np
import cv2

# LED-Konfiguration (Anpassen an dein Setup)
LED_COUNT = 220
PIN = board.D18
LED_BRIGHTNESS = 0.7

# Initialize NeoPixel object
pixels = neopixel.NeoPixel(PIN, LED_COUNT, brightness=0.7, auto_write=False)

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

if not cap.isOpened():
    print("Fehler: HDMI-Capture-Device nicht gefunden!")
    exit()

def get_dominant_color(q):
    ret, frame = cap.read()
    if not ret:
        print("Kein HDMI-Signal!")
        return

    while True:
        ret, frame = cap.read()
        resized = cv2.resize(frame, (70, 40), interpolation=cv2.INTER_LINEAR)
        q.put(resized)

def update_leds(q):
    """ LEDs aktualisieren """
    while True:
        colors = q.get()
        for i in range(LED_COUNT):
            if(i >= 150):
                pixels[i] = colors[i - 150-1, 40-1]
            elif(i >= 110):
                pixels[i] = colors[70-1, i - 110-1]
            elif(i >= 40):
                pixels[i] = colors[i - 40-1, 1-1]
            else:
                pixels[i] = colors[1-1, i]
        pixels.show()
        print("LEDs Updated")

if __name__ == "__main__":
    q = mp.Queue()

    p1 = mp.Process(target=get_dominant_color, args=(q,))
    p2 = mp.Process(target=update_leds, args=(q,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
