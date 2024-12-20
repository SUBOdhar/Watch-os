"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Raspberry Pi Pico SSD1306 OLED Display (MicroPython)     ┃
┃                                                          ┃
┃ A program to display a watch face with large blocky      ┃
┃ numbers on an SSD1306 OLED display connected to a        ┃
┃ Raspberry Pi Pico.                                       ┃
┃                                                          ┃
┃ Copyright (c) 2023 Anderson Costa                        ┃
┃ GitHub: github.com/arcostasi                             ┃
┃ License: MIT                                             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import sys
import urandom
import utime

# Pixel resolution for the OLED display
pix_res_x = 128
pix_res_y = 64

def init_i2c(scl_pin, sda_pin):
    # Initialize I2C device
    i2c_dev = I2C(1, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=200000)
    i2c_addr = [hex(ii) for ii in i2c_dev.scan()]
    
    # Check if any I2C device is found
    if not i2c_addr:
        print('No I2C Display Found')
        sys.exit()
    else:
        print("I2C Address      : {}".format(i2c_addr[0]))
        print("I2C Configuration: {}".format(i2c_dev))
    
    return i2c_dev

def draw_large_digit(oled, digit, x, y):
    # Define patterns for each large digit (24x24)
    patterns = {
        '0': ["########################",
              "########################",
              "########      ##########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "########      ##########",
              "########################",
              "########################",
              "########################",
              "########################"],
        '1': ["          ####          ",
              "        ######          ",
              "      ########          ",
              "          ####          ",
              "          ####          ",
              "          ####          ",
              "          ####          ",
              "          ####          ",
              "          ####          ",
              "          ####          ",
              "          ####          ",
              "          ####          ",
              "          ####          ",
              "          ####          ",
              "          ####          ",
              "          ####          ",
              "          ####          ",
              "          ####          ",
              "          ####          ",
              "          ####          ",
              "  ######################",
              "  ######################",
              "  ######################",
              "  ######################"],
        '2': ["########################",
              "########################",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "########################",
              "########################",
              "########################",
              "############            ",
              "############            ",
              "############            ",
              "############            ",
              "############            ",
              "############            ",
              "############            ",
              "########################",
              "########################",
              "########################",
              "########################"],
        '3': ["########################",
              "########################",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "########################",
              "########################",
              "########################",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "########################",
              "########################",
              "########################",
              "########################"],
        '4': ["######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "########################",
              "########################",
              "########################",
              "########################",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############"],
        '5': ["########################",
              "########################",
              "######                  ",
              "######                  ",
              "######                  ",
              "######                  ",
              "######                  ",
              "######                  ",
              "######                  ",
              "######                  ",
              "########################",
              "########################",
              "########################",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "########################",
              "########################",
              "########################",
              "########################"],
        '6': ["########################",
              "########################",
              "######                  ",
              "######                  ",
              "######                  ",
              "######                  ",
              "######                  ",
              "######                  ",
              "######                  ",
              "######                  ",
              "########################",
              "########################",
              "########################",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "########################",
              "########################",
              "########################",
              "########################"],
              
        '7': ["########################",
              "########################",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############"],
        '8': ["########################",
              "########################",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "########################",
              "########################",
              "########################",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "########################",
              "########################",
              "########################",
              "########################"],
        '9': ["########################",
              "########################",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "######          ########",
              "########################",
              "########################",
              "########################",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "            ############",
              "########################",
              "########################",
              "########################",
              "########################"],
    }
    
    pattern = patterns[digit]
    for row in range(24):
        for col in range(24):
            if pattern[row][col] == '#':
                oled.pixel(x + col, y + row, 1)

def get_random_time():
    # Generate random hour and minute
    hour = urandom.randint(0, 23)
    minute = urandom.randint(0, 59)
    return hour, minute

def display_watch_face(oled):
    while True:
        # Get a random time
        hour, minute = get_random_time()
        
        # Format the hour and minute
        hour_str = "{:02}".format(hour)
        minute_str = "{:02}".format(minute)
        
        # Clear the display
        oled.fill(0)
        
        # Center the time on the display
        x_offset = 0
        y_offset = 8
        
        # Draw hours
        draw_large_digit(oled, hour_str[0], x_offset, y_offset)
        draw_large_digit(oled, hour_str[1], x_offset + 28, y_offset)

        
        # Draw minutes
        draw_large_digit(oled, minute_str[0], 58, 32)
        draw_large_digit(oled, minute_str[1], 92, 32)
        
        oled.show()
        utime.sleep(10)  # Update the time every 10 seconds for demonstration

def main():
    i2c_dev = init_i2c(scl_pin=27, sda_pin=26)
    oled = SSD1306_I2C(pix_res_x, pix_res_y, i2c_dev)
    display_watch_face(oled)

if __name__ == '__main__':
    main()
