import multiprocessing as mp
import board
import neopixel
import time
import mss
import numpy as np
import cv2
import queue
import json

# LED-Konfiguration
with open("config.json", "r") as file:
    data = json.load(file)

LED_COUNT_LEFT = data["count_left"]
LED_COUNT_TOP = data["count_top"]
LED_COUNT_RIGHT = data["count_right"]
LED_COUNT_BOTTOM = data["count_bottom"]
LED_BRIGHTNESS = data["brightness"]
LED_COUNT = LED_COUNT_BOTTOM + LED_COUNT_RIGHT + LED_COUNT_TOP + LED_COUNT_LEFT
LED_OFFSET = data["offset"]
PIN = board.D18

WAIT = 0.0016

def update_variables(){
    while True:
        with open("config.json", "r") as file:
            data = json.load(file)

        LED_COUNT_LEFT = data["count_left"]
        LED_COUNT_TOP = data["count_top"]
        LED_COUNT_RIGHT = data["count_right"]
        LED_COUNT_BOTTOM = data["count_bottom"]
        LED_BRIGHTNESS = data["brightness"]
        LED_COUNT = LED_COUNT_BOTTOM + LED_COUNT_RIGHT + LED_COUNT_TOP + LED_COUNT_LEFT
        LED_OFFSET = data["offset"]
}

def get_smooth_color(c1, c2, ratio=0.6):
    return np.rint(np.array(c1)*ratio + np.array(c2)*(1-ratio)).astype(int).tolist()

# Initialize NeoPixel object
pixels = neopixel.NeoPixel(PIN, LED_COUNT, brightness=1, auto_write=False)

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

old_pixels = [[0,0,0]] * LED_COUNT

if not cap.isOpened():
    print("Fehler: HDMI-Capture-Device nicht gefunden!")
    exit()

def get_screen(q):
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Kein HDMI-Signal!")
            exit()
        q.put(frame)
        time.sleep(WAIT)

#TODO: resized_height und resized_width -> einmal langegestreckt in die eine und dann in die anderen richtung
def get_dominant_color(q_in, q_out):
    while True:
        try:
            frame = q_in.get_nowait()
            resized = cv2.resize(frame, (70, 40), interpolation=cv2.INTER_LINEAR)
            print(resized[0,0].tolist())
            q_out.put_nowait(resized)
            time.sleep(WAIT)
        except mp.queues.Empty:
            pass

#TODO: leds immer updaten wenn neuer input
#TODO: chatGPT while not queue.empty()
def update_leds(q):
    """ LEDs aktualisieren """
    while True:
        try:
            colors = q.get_nowait()
            for i in range(LED_COUNT):
                if(i >= 150):
                    color = colors[37, 69 - (i - 150)]
                    pixels[i] = bgr_to_rgb(color.tolist())  # Pass as list
                elif(i >= 110):
                    color = colors[i - 110, 67]
                    pixels[i] = bgr_to_rgb(color.tolist())  # Pass as list
                elif(i >= 40):
                    color = colors[2, i - 40]
                    pixels[i] = bgr_to_rgb(color.tolist())  # Pass as list
                else:
                    color = colors[39 - i, 2]
                    pixels[i] = bgr_to_rgb(color.tolist())  # Pass as list
            pixels[:] = get_smooth_color(old_pixels, pixels)
            old_pixels[:] = pixels
            pixels.show()
            print("LEDs Updated")
            time.sleep(WAIT)
        except KeyboardInterrupt:
            pixels.fill((0,0,0))
            pixels.show()
            exit()
        except mp.queues.Empty:
            pass

def bgr_to_rgb(color):
    return (round(color[2]), round(color[1]), round(color[0]))

if __name__ == "__main__":
    q_screen = mp.Queue()
    q_colors = mp.Queue()

    p_get_screen = mp.Process(target=get_screen, args=(q_screen,))
    p_dominant_colors = mp.Process(target=get_dominant_color, args=(q_screen, q_colors))
    p_update_leds = mp.Process(target=update_leds, args=(q_colors,))
    p_update_variables = mp.Process(target=update_variables)

    p_get_screen.start()
    p_dominant_colors.start()
    p_update_leds.start()
    p_update_variables.start()

    p_update_variables.join()
    p_get_screen.join()
    p_dominant_colors.join()
    p_update_leds.join()
