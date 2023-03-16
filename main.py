from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import time
import math
from selenium.webdriver.chrome.options import Options
from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from discord import Webhook, RequestsWebhookAdapter
#player-overlay-mature-accept
# Set the Chrome options to start the browser maximized
CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
WINDOW_SIZE = "1920,1080"
chrome_options = Options()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument('--no-sandbox')

# Start the Chrome browser with the options
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                          chrome_options=chrome_options
                         )

# Navigate to the Twitch channel and wait for the page to load
driver.get('https://www.twitch.tv/videos/1766004801')
sleep(5)  # Wait for 5 seconds to allow the page to fully load

# Find and click the "Zaakceptuj pliki cookie" button to dismiss the cookie banner
# Find and click the "Zaakceptuj pliki cookie" button to dismiss the cookie banner
actions = ActionChains(driver)
wait = WebDriverWait(driver, 5)
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-a-target="player-overlay-mature-accept"]')))

# click the button
button.click()
actions.send_keys('f').perform()

# Take a screenshot of the webpage and save it as a file named "screenshot.png"
send_cooldown=0
while True:
    # Your code here
    driver.get_screenshot_as_file("screenshot.png")
  


    # Open the JPEG file
    with Image.open("screenshot.png") as img:
        # Convert the image to the RGB color space
        img = img.convert("RGB")

        # Get the dimensions of the image
        width, height = img.size

        # Initialize counters for red, green, and blue pixels
        red_count = 0
        green_count = 0
        blue_count = 0

        # Iterate over each pixel in the image
        for x in range(width):
            for y in range(height):
                # Get the RGB values for the pixel
                r, g, b = img.getpixel((x, y))

                # Increment the appropriate counter based on the dominant color component
                if r > g and r > b:
                    red_count += 1
                elif g > r and g > b:
                    green_count += 1
                else:
                    blue_count += 1

    pixel_sum=green_count+red_count+blue_count
    red_count=math.ceil((red_count/pixel_sum)*100)
    green_count=math.ceil((green_count/pixel_sum)*100)
    blue_count=math.ceil((blue_count/pixel_sum)*100)
    
    print("Red pixels:", red_count)
    print("Green pixels:", green_count)
    print("Blue pixels:", blue_count)
    print("Blue pixels:", send_cooldown)

    if red_count>70 and send_cooldown==0:
        webhook = Webhook.from_url("https://discord.com/api/webhooks/1085887517292761189/ctEiIk2FHrHm7SnQeFGjlZNCNFNAA0hmUi4rO3z-ehTNA2TAieCGPmwHW1h3ZDSrVxkw", adapter=RequestsWebhookAdapter())
        webhook.send("Hello World")
        send_cooldown=300
    # Pause the script for 5 seconds
    if send_cooldown > 0:
        send_cooldown-=5
    time.sleep(5)


# Close the browser

