from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import configparser
import time
import discord
from PIL import ImageEnhance
import PIL
import pytesseract
import selenium
#Opcje chroma
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")

#Czytaj konfig
config = configparser.ConfigParser()
config.read('config.ini')
value = config.get('discord', 'webhook_link')
kanal = config.get('stream', 'kanal')

#odpal chroma
driver = selenium.webdriver.Chrome(options=chrome_options, executable_path='/usr/local/bin/chromedriver')

#link do webhooka discorda
webdiscordlink=value

#Wejdź na kanał i poczekaj
driver.get(kanal)
time.sleep(5)

#przeklikanie przez popupy
wait = WebDriverWait(driver, 15)
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-a-target="player-overlay-mature-accept"]')))
button.click()
#button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-test-selector="muted-segments-alert-overlay-presentation__dismiss-button"]')))
#button.click()
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-a-target="player-settings-button"]')))
button.click()
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-a-target="player-settings-menu-item-quality"')))
button.click()
checkbox = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-a-target="player-settings-submenu-quality-option"]')))
checkbox[1].click()


#kordy do cropa
send_cooldown=0
x1, y1 = 556, 884
x2, y2 = 861, 907

x12, y12 = 1413, 289
x22, y22 = 1561, 310

x13, y13 = 241, 234
x23, y23 = 1579, 987

#czego szukamy
words_to_check = ["cen't",'see','this','shit','mist']


#pantal typu gigachad
while True:
    if send_cooldown == 0:
        driver.get_screenshot_as_file("screenshoty/screenshot.png")
        img = PIL.Image.open('screenshoty/screenshot.png')
        cropped_img = img.crop((x1, y1, x2, y2))
        cropped_img = cropped_img.convert('L')
        enchancer = ImageEnhance.Contrast(cropped_img)
        factor = 1.5
        im_output = enchancer.enhance(factor)
        im_output.save('screenshoty/cropped_img.png')
        text = pytesseract.image_to_string(cropped_img, lang='mc')
        print(f'\rText: {text}', end='')
        


        num_words_found = 0
        for word in words_to_check:
            if word in text:
                num_words_found += 1
                if num_words_found >= 2:
                    wynik = img.crop((x13, y13, x23, y23))
                    wynik.save('screenshoty/wynik.png')
                    print("Nether detected sending, notification to discord")
                    webhook = discord.SyncWebhook.from_url(webdiscordlink)
                    embed = discord.Embed()
                    embed.description = "Forsen jest w nether [stream](https://www.twitch.tv/forsen)" 
                    webhook.send(embed=embed, file=discord.File('screenshoty/wynik.png'))
                    send_cooldown=150
                    break
        
    else:
        print(f'\rCooldown: {send_cooldown}', end='')
        
    if send_cooldown >= 1:
        send_cooldown-=1
    elif send_cooldown <1:
        send_cooldown = send_cooldown - send_cooldown
    time.sleep(1)

