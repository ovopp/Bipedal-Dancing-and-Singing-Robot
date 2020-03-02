"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text.
"""

import board
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_st7735r import ST7735R

# Release any resources currently in use for the displays
displayio.release_displays()

spi = board.SPI()
tft_cs = board.A2
tft_dc = board.A4

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.A3)

display = ST7735R(display_bus, width=128, height=128, colstart=2, rowstart=1)

# Make the display context

# Open the file
with open("/purple.bmp", "rb") as bitmap_file:
 
    # Setup the file as the bitmap data source
    bitmap = displayio.OnDiskBitmap(bitmap_file)
 
    # Create a TileGrid to hold the bitmap
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())
 
    # Create a Group to hold the TileGrid
    group = displayio.Group()
 
    # Add the TileGrid to the Group
    group.append(tile_grid)
 
    # Add the Group to the Display
    display.show(group)
 
    # Loop forever so you can enjoy your image
while True:
  pass
