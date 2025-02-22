import board
import neopixel

# Initialize NeoPixel object
pixels = neopixel.NeoPixel(PIN, LED_COUNT, brightness=1, auto_write=False)

# LED configuration
with open("config.json", "r") as file:
    data = json.load(file)

LED_COUNT_LEFT = data["count_left"]
LED_COUNT_TOP = data["count_top"]
LED_COUNT_RIGHT = data["count_right"]
LED_COUNT_BOTTOM = data["count_bottom"]
LED_COUNT = LED_COUNT_BOTTOM + LED_COUNT_RIGHT + LED_COUNT_TOP + LED_COUNT_LEFT
PIN = board.D18

pixels.fill((0,0,0))
pixels.show()
exit