from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import time
import discord
import math
from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains
from discord import SyncWebhook
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
#player-overlay-mature-accept
# Set the Chrome options to start the browser maximized
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options, executable_path='/usr/local/bin/chromedriver')

# Navigate to the Twitch channel and wait for the page to load
driver.get('https://www.twitch.tv/lpl')
sleep(5)  # Wait for 5 seconds to allow the page to fully load

# Find and click the "Zaakceptuj pliki cookie" button to dismiss the cookie banner
# Find and click the "Zaakceptuj pliki cookie" button to dismiss the cookie banner

#wait = WebDriverWait(driver, 15)
#button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-a-target="player-overlay-mature-accept"]')))
#button.click()


# Take a screenshot of the webpage and save it as a file named "screenshot.png"
send_cooldown=0
# Define the coordinates of the rectangle
left = 240
top = 234
right = 1579
bottom = 987
pixel_sum = (right - left) * (bottom - top)
while True:
    # Your code here
    driver.get_screenshot_as_file("screenshot.png")
  


    # Open the JPEG file
    with Image.open("screenshot.png") as img:
        # Convert the image to the RGB color space
        img = img.convert("RGB")



        # Initialize counters for red, green, and blue pixels
        red_count = 0
        green_count = 0
        blue_count = 0

        # Iterate over each pixel within the defined rectangle
        for x in range(left, right):
            for y in range(top, bottom):
                # Get the RGB values for the pixel
                r, g, b = img.getpixel((x, y))

                # Increment the appropriate counter based on the dominant color component
                if r > g and r > b:
                    red_count += 1
                elif g > r and g > b:
                    green_count += 1
                else:
                    blue_count += 1

    
    red_count=math.ceil((red_count/pixel_sum)*100)
    green_count=math.ceil((green_count/pixel_sum)*100)
    blue_count=math.ceil((blue_count/pixel_sum)*100)
    
    print(f"\rRed pixels: {red_count}%  Green pixels: {green_count}%  Blue pixels: {blue_count}%  Cooldown: {send_cooldown}s", end='', flush=True)

    if red_count>80 and send_cooldown==0:
        webhook = SyncWebhook.from_url("https://discord.com/api/webhooks/1086234013485772871/lPIWQeiTeRjIH50lBTGwlvzyj_0Y8ob8skSMyg154bdl51xlRDvJGp2jPW94n5VSv0VA")
        webhook.send("Na ekranie Forsena jest czerwono... chyba jest w netherze")
        webhook.send(file=discord.File('screenshot.png'))

        send_cooldown=600
    
    if send_cooldown >= 2:
        send_cooldown-=2
    elif send_cooldown <2:
        send_cooldown = send_cooldown - send_cooldown
    #time.sleep(2)


# Close the browser

