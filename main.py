from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time
from time import sleep

import discord


from PIL import Image
from PIL import ImageEnhance
import pytesseract

# Set the Chrome options to start the browser maximized
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options, executable_path='/usr/local/bin/chromedriver')
webdiscordlink="https://discord.com/api/webhooks/1086234013485772871/lPIWQeiTeRjIH50lBTGwlvzyj_0Y8ob8skSMyg154bdl51xlRDvJGp2jPW94n5VSv0VA"
# Navigate to the Twitch channel and wait for the page to load
driver.get('https://www.twitch.tv/videos/1764155703?t=04h23m59s')
sleep(5)  # Wait for 5 seconds to allow the page to fully load

wait = WebDriverWait(driver, 15)
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-a-target="player-overlay-mature-accept"]')))
button.click()
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-test-selector="muted-segments-alert-overlay-presentation__dismiss-button"]')))
button.click()

button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-a-target="player-settings-button"]')))
button.click()
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-a-target="player-settings-menu-item-quality"')))
button.click()


checkbox = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-a-target="player-settings-submenu-quality-option"]')))

checkbox[1].click()
#data-a-target="player-settings-button"
#data-a-target="player-settings-menu-item-quality"
#class="ScCheckBoxInputBase-sc-vu7u7d-1 gBDDIa tw-radio__input"


send_cooldown=0
x1, y1 = 556, 884
x2, y2 = 861, 907

x12, y12 = 1296, 246
x22, y22 = 1567, 290

words_to_check = ["can't",'see','this','shit','mist']

while True:
    if send_cooldown == 0:
        driver.get_screenshot_as_file("screenshot.png")
    


        # Open the JPEG file
        img = Image.open('screenshot.png')
        cropped_img = img.crop((x1, y1, x2, y2))
       # cropped_img2 = img.crop((x12, y12, x22, y22))

        # Convert the cropped image to grayscale
        cropped_img = cropped_img.convert('L')
        enchancer = ImageEnhance.Contrast(cropped_img)
        factor = 1.5
        im_output = enchancer.enhance(factor)
        im_output.save('cropped_img.png')
       # cropped_img2 = cropped_img2.convert('L')
       # cropped_img2.save('cropped_img2.png')
        text = pytesseract.image_to_string(cropped_img)
       # text2 = pytesseract.image_to_string(cropped_img2)
        print(f'\rText: {text}', end='')
       # print(f'\rText2: {text2}', end='')


        num_words_found = 0
        for word in words_to_check:
            if word in text:
                num_words_found += 1
                if num_words_found >= 2:
                    print("Nether detected sending Notification to discord")
                    webhook = discord.SyncWebhook.from_url(webdiscordlink)
                    embed = discord.Embed()
                    embed.description = "Forsen jest w nether [stream](https://www.twitch.tv/forsen)."
                    webhook.send(embed=embed, file=discord.File('screenshot.png'))
                   # webhook.send(file=discord.File('screenshot.png'))
                    #webhook.send("Forsen jest w nether")
                    #webhook.send(file=discord.File('screenshot.png'))
                    send_cooldown=20
                    break
    else:
        print(f'\rCooldown: {send_cooldown}', end='')
        
    if send_cooldown >= 1:
        send_cooldown-=1
    elif send_cooldown <1:
        send_cooldown = send_cooldown - send_cooldown
    time.sleep(1)


# Close the browser

