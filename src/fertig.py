import multiprocessing as mp
import board
import neopixel
import time
import mss
import numpy as np
import cv2
import queue

# LED-Konfiguration (Anpassen an dein Setup)
LED_COUNT = 220
PIN = board.D18
LED_BRIGHTNESS = 0.7

WAIT = 0.01

# Initialize NeoPixel object
pixels = neopixel.NeoPixel(PIN, LED_COUNT, brightness=0.7, auto_write=False)

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

if not cap.isOpened():
    print("Fehler: HDMI-Capture-Device nicht gefunden!")
    exit()

def get_screen(q):
    ret, frame = cap.read()
    if not ret:
        print("Kein HDMI-Signal!")
        exit()
    q.put(frame)

def get_dominant_color(q):
    while True:
        frame = q_in.get()
        resized = cv2.resize(frame, (70, 40), interpolation=cv2.INTER_LINEAR)
        print(resized[0,0].tolist())
        q_out.put(resized)

def update_leds(q):
    """ LEDs aktualisieren """
    while True:
        try:
            colors = q.get_nowait()
            for i in range(LED_COUNT):
                if(i >= 150):
                    color = colors[39, i - 150]
                    pixels[i] = bgr_to_rgb(color.tolist())  # Pass as list
                elif(i >= 110):
                    color = colors[i - 110, 69]
                    pixels[i] = bgr_to_rgb(color.tolist())  # Pass as list
                elif(i >= 40):
                    color = colors[0, i - 40]
                    pixels[i] = bgr_to_rgb(color.tolist())  # Pass as list
                else:
                    color = colors[i, 0]
                    pixels[i] = bgr_to_rgb(color.tolist())  # Pass as list
            pixels.show()
            print("LEDs Updated")
        except KeyboardInterrupt:
            pixels.fill((0,0,0))
            pixels.show()
            exit()
        except mp.queues.Empty:
            pass

def bgr_to_rgb(color):
    return (round(color[2]), round(color[0]), round(color[1]))

if __name__ == "__main__":
    q_screen = mp.Queue()
    q_colors = mp.Queue()

    p1 = mp.Process(target=get_dominant_color, args=(q_screen,))
    p2 = mp.Process(target=get_dominant_color, args=(q_screen, q_colors))
    p3 = mp.Process(target=update_leds, args=(q_colors,))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()