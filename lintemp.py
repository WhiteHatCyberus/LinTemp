import subprocess
import time
from PIL import Image, ImageDraw
import re

BAR_WIDTH = 200  # Width of the temperature bar
BAR_HEIGHT = 20  # Height of the temperature bar
BORDER_WIDTH = 2  # Width of the bar borders
REFRESH_RATE = 1  # Refresh rate in seconds

def get_cpu_temperature():
    result = subprocess.run(['sensors'], capture_output=True, text=True)
    output = result.stdout

    temperature_line = re.search(r'Package.*?\+(\d+\.\d+)', output)
    if temperature_line:
        temperature = float(temperature_line.group(1))
        return temperature

    return None

# Create an empty image with a transparent background
image = Image.new('RGBA', (BAR_WIDTH, BAR_HEIGHT), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)

def update_temperature_bar():
    temperature = get_cpu_temperature()
    if temperature is not None:
        bar_fill = int((temperature / 100.0) * BAR_WIDTH)

        # Draw the border of the bar with partial transparency
        border_color = (255, 255, 255, 100)  # White with transparency (adjust the alpha value as desired)
        draw.rectangle((0, 0, BAR_WIDTH - 1, BAR_HEIGHT - 1), outline=border_color, width=BORDER_WIDTH)

        # Draw the filled portion of the bar with partial transparency
        if temperature >= 80:
            fill_color = (255, 0, 0, 150)  # Red with transparency
        elif temperature < 40:
            fill_color = (0, 0, 255, 150)  # Blue with transparency
        else:
            fill_color = (0, 255, 0, 150)  # Green with transparency
        draw.rectangle((BORDER_WIDTH, BORDER_WIDTH, bar_fill, BAR_HEIGHT - BORDER_WIDTH), fill=fill_color)

        # Draw the temperature text inside the bar
        temperature_text = f"{temperature}°C"
        temperature_text_color = (255, 255, 255)  # White
        text_bbox = draw.textbbox((0, 0), temperature_text)
        text_position = ((BAR_WIDTH - text_bbox[2]) // 2, (BAR_HEIGHT - text_bbox[3]) // 2)
        draw.text(text_position, temperature_text, fill=temperature_text_color)

        # Save the image to the local filesystem
        image_path = '/tmp/temperature_bar.png'
        image.save(image_path)
        print(f"{temperature}°C")

while True:
    update_temperature_bar()
    time.sleep(REFRESH_RATE)
