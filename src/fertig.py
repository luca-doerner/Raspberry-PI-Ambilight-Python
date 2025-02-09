import multiprocessing as mp
import time
import mss
import numpy as np
import cv2
from rpi_ws281x import PixelStrip, Color  # Falls du WS2812 LEDs nutzt

# LED-Konfiguration (Anpassen an dein Setup)
LED_COUNT = 220
LED_PIN = 18
LED_BRIGHTNESS = 150

# LED-Strip initialisieren
strip = PixelStrip(LED_COUNT, LED_PIN, brightness=LED_BRIGHTNESS)
strip.begin()

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

if not cap.isOpened():
    print("Fehler: HDMI-Capture-Device nicht gefunden!")
    exit()

def get_dominant_color():
    ret, frame = cap.read()
    if not ret:
        print("Kein HDMI-Signal!")
        return

    resized = cv2.resize(frame, (1, 1), interpolation=cv2.INTER_LINEAR)
    colors = resized[0, 0].toList()
    q_out.put(colors)

def update_leds(q):
    """ LEDs aktualisieren """
    while True:
        colors = q.get()
        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(int(colors[2]), int(colors[1]), int(colors[0])))  # BGR zu RGB
        strip.show()
        print("LEDs Updated")

if __name__ == "__main__":
    q_screen = mp.Queue()
    q_colors = mp.Queue()

    p1 = mp.Process(target=get_dominant_color(), args=(q_screen,))
    p2 = mp.Process(target=update_leds, args=(q_colors,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
