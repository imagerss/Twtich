from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import time
from discord import SyncWebhook
import discord
from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains
import pytesseract
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
webdiscordlink=""
# Navigate to the Twitch channel and wait for the page to load
driver.get('https://www.twitch.tv/videos/1764155703?t=02h53m04s')
sleep(5)  # Wait for 5 seconds to allow the page to fully load

# Find and click the "Zaakceptuj pliki cookie" button to dismiss the cookie banner
# Find and click the "Zaakceptuj pliki cookie" button to dismiss the cookie banner

wait = WebDriverWait(driver, 15)
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-a-target="player-overlay-mature-accept"]')))
button.click()
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-test-selector="muted-segments-alert-overlay-presentation__dismiss-button"]')))
button.click()

# Take a screenshot of the webpage and save it as a file named "screenshot.png"
send_cooldown=0
x1, y1 = 556, 882
x2, y2 = 861, 905

x12, y12 = 1296, 246
x22, y22 = 1567, 290

words_to_check = ["can't",'I','see','shit','mist']
# Define the coordinates of the rectangle
while True:
    if send_cooldown == 0:
        driver.get_screenshot_as_file("screenshot.png")
    


        # Open the JPEG file
        img = Image.open('screenshot.png')
        cropped_img = img.crop((x1, y1, x2, y2))
        cropped_img2 = img.crop((x12, y12, x22, y22))

        # Convert the cropped image to grayscale
        cropped_img = cropped_img.convert('L')
        cropped_img.save('cropped_img.png')
        cropped_img2 = cropped_img2.convert('L')
        cropped_img2.save('cropped_img2.png')
        text = pytesseract.image_to_string(cropped_img)
        text2 = pytesseract.image_to_string(cropped_img2)
        print(f'\rText: {text}', end='')
        print(f'\rText2: {text2}', end='')


        num_words_found = 0
        for word in words_to_check:
            if word in text or word in text2:
                num_words_found += 1
                if num_words_found >= 1:
                    print("Nether detected sending Notification to discord")
                    webhook = SyncWebhook.from_url(webdiscordlink)
                    embed = discord.Embed()
                    embed.description = "Forsen jest w nether [stream](https://www.twitch.tv/forsen)."
                    webhook.send(embed=embed)
                    webhook.send(file=discord.File('screenshot.png'))
                    #webhook.send("Forsen jest w nether")
                    #webhook.send(file=discord.File('screenshot.png'))
                    send_cooldown=600
                    break
    else:
        print(f'\rCooldown: {send_cooldown}s', end='')
        
    if send_cooldown >= 1:
        send_cooldown-=1
    elif send_cooldown <1:
        send_cooldown = send_cooldown - send_cooldown
    time.sleep(1)


# Close the browser

