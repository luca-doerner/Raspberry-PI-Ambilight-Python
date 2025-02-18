import multiprocessing as mp
import board
import neopixel
import time
import numpy as np
import cv2
import json
import threading

# LED-Konfiguration (Anpassen an dein Setup)
PIN = board.D18

WAIT = 0.02

with open("config.json", "r") as file:
    data = json.load(file)

LED_COUNT_LEFT = data["count_left"]
LED_COUNT_TOP = data["count_top"]
LED_COUNT_RIGHT = data["count_right"]
LED_COUNT_BOTTOM = data["count_bottom"]
LED_BRIGHTNESS = data["brightness"]
LED_COUNT = LED_COUNT_BOTTOM + LED_COUNT_RIGHT + LED_COUNT_TOP + LED_COUNT_LEFT
LED_OFFSET = data["offset"]

# Initialize NeoPixel object
pixels = neopixel.NeoPixel(PIN, LED_COUNT, brightness=LED_BRIGHTNESS, auto_write=False)

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

if not cap.isOpened():
    cap = cv2.VideoCapture(1, cv2.CAP_V4L2)
    if not cap.isOpened():
        print("Fehler: HDMI-Capture-Device nicht gefunden!")
        exit()

def get_screen(q):
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Kein HDMI-Signal!")
            exit()
        q.put_nowait(frame)

def get_dominant_color(q_in, q_out, x, y):
    while True:
        try:
            frame = q_in.get_nowait()
            resized = cv2.resize(frame, (x, y), interpolation=cv2.INTER_LINEAR)
            q_out.put_nowait(resized)
        except mp.queues.Empty:
            pass


def update_leds(q, previous_count, count, side):
    while True:
        short_side = False
        padding = 0

        if side == "left":
            short_side = True
            padding = 2
        elif side == "top":
            padding = 2
        elif side == "right":
            short_side = True
            padding = 8
        elif side == "bottom":
            padding = 8

        start = previous_count-LED_OFFSET
        end = start+count

        start_invert = 0
        end_invert = 0
        if start < 0:
            start_invert = LED_COUNT+start
            end_invert = LED_COUNT
            start = 0

        try:
            colors = q.get_nowait()
            print(f"Updating side {side} with {len(colors)} colors")
            for i in range(start, end):
                color = get_pixel_color(i, start, end, side, count, colors)
                pixels[i] = bgr_to_rgb(color)

            for i in range(start_invert, end_invert):
                color = get_pixel_color(i, start, end, side, count, colors)
                pixels[i] = bgr_to_rgb(color)
        except mp.queues.Empty:
            pass

def get_pixel_color(i, start, end, side, count, colors):
    if side == "left":
        color = colors[count-(i-start+1), 2]
    elif side == "top":
        color = colors[2, i-start-1]
    elif side == "right":
        color = colors[i-start-1, 8]
    elif side == "bottom":
        color = colors[8, count-(i-start+1)]
    return color

# Neuer Thread zum regelmäßigen `pixels.show()`
def led_updater():
    while True:
        time.sleep(0.01)  # Kurzes Delay, um die CPU nicht zu überlasten
        pixels.show()

# Startet den LED-Update-Thread
t_led_updater = threading.Thread(target=led_updater, daemon=True)
t_led_updater.start()

def bgr_to_rgb(color):
    return (round(color[2]), round(color[1]), round(color[0]))

if __name__ == "__main__":
    q_screen = mp.Queue()
    q_color_left = mp.Queue()
    q_color_top = mp.Queue()
    q_color_right = mp.Queue()
    q_color_bottom = mp.Queue()

    p_screen = mp.Process(target=get_screen, args=(q_screen,))

    p_color_left = mp.Process(target=get_dominant_color, args=(q_screen, q_color_left, 11, LED_COUNT_LEFT))
    p_color_top = mp.Process(target=get_dominant_color, args=(q_screen, q_color_top, LED_COUNT_TOP, 11))
    p_color_right = mp.Process(target=get_dominant_color, args=(q_screen, q_color_right, 11, LED_COUNT_RIGHT))
    p_color_bottom = mp.Process(target=get_dominant_color, args=(q_screen, q_color_bottom, LED_COUNT_BOTTOM, 11))

    p_led_left = mp.Process(target=update_leds, args=(
        q_color_left,
        0,
        LED_COUNT_LEFT,
        "left"))
    p_led_top = mp.Process(target=update_leds, args=(
        q_color_top,
        LED_COUNT_LEFT,
        LED_COUNT_TOP,
        "top"))
    p_led_right = mp.Process(target=update_leds, args=(
        q_color_right,
        LED_COUNT_LEFT+LED_COUNT_TOP,
        LED_COUNT_RIGHT,
        "right"))
    p_led_bottom = mp.Process(target=update_leds, args=(
        q_color_bottom,
        LED_COUNT_LEFT+LED_COUNT_TOP+LED_COUNT_RIGHT,
        LED_COUNT_BOTTOM,
        "bottom"))

    p_screen.start()

    p_color_left.start()
    p_color_top.start()
    p_color_right.start()
    p_color_bottom.start()

    p_led_left.start()
    p_led_top.start()
    p_led_right.start()
    p_led_bottom.start()


    p_screen.join()

    p_color_left.join()
    p_color_top.join()
    p_color_right.join()
    p_color_bottom.join()

    p_led_left.join()
    p_led_top.join()
    p_led_right.join()
    p_led_bottom.join()