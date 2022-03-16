from neopixel import NeoPixel
from machine import Pin
import time

# Setup neopixels
LED_PIN = 21
NUM_LEDS = 75
pixels = NeoPixel(Pin(LED_PIN), NUM_LEDS)

# takes HSV, returns RGB
def colorHSV(hue, sat, val):
        if hue >= 65536:
            hue %= 65536

        hue = (hue * 1530 + 32768) // 65536
        if hue < 510:
            b = 0
            if hue < 255:
                r = 255
                g = hue
            else:
                r = 510 - hue
                g = 255
        elif hue < 1020:
            r = 0
            if hue < 765:
                g = 255
                b = hue - 510
            else:
                g = 1020 - hue
                b = 255
        elif hue < 1530:
            g = 0
            if hue < 1275:
                r = hue - 1020
                b = 255
            else:
                r = 255
                b = 1530 - hue
        else:
            r = 255
            g = 0
            b = 0

        v1 = 1 + val
        s1 = 1 + sat
        s2 = 255 - sat

        r = ((((r * s1) >> 8) + s2) * v1) >> 8
        g = ((((g * s1) >> 8) + s2) * v1) >> 8
        b = ((((b * s1) >> 8) + s2) * v1) >> 8

        return (r, g, b)

# set RGB colour
def setRGB(rgb_tuple):
    for i in range(NUM_LEDS):
        pixels[i] = rgb_tuple
    pixels.write()
    
# candy unicorn rainbow aka Niagara Falls
def setNiagara(sat=255, val=255, delay_ms=50, hue_gap=65535//NUM_LEDS, hue_cycle_speed=65535//NUM_LEDS):
    sync_hue = 0
    
    while True:
        hue = sync_hue
        for i in range(NUM_LEDS):
            pixels[i] = colorHSV(hue, sat, val)
            hue = (hue + hue_gap) % 65536
        
        sync_hue = (sync_hue + hue_cycle_speed) % 65536
        
        pixels.write()
        time.sleep_ms(delay_ms)
        