import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from bs4 import BeautifulSoup
from pynput.keyboard import Key, Controller
import requests

f = open("myAccounts.txt")
lines = f.readlines()
username_file = lines[0]
password_file = lines[1]
f.close()
date = str(datetime.datetime.now().strftime("%d.%m.%Y"))
prefix = "[" + str(datetime.datetime.now().strftime("%H:%M:%S")) + "] " + "[Corona-Updater] "


def get_numbers():
    driver = webdriver.Chrome(executable_path='/Users/nicowerner/Documents/Programmieren/python/Corona/chromedriver')
    driver.get("https://www.corona-in-zahlen.de/landkreise/lk%20ostalbkreis/")
    print(prefix + "going to https://www.corona-in-zahlen.de/landkreise/lk%20ostalbkreis/")
    sleep(2)
    infections = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[2]/div/div/p[1]/b')
    infection_rate = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[3]/div/div/p[1]/b')
    death_cases = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[5]/div/div/p[1]/b")
    Inzidenz = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[4]/div/div/p[1]/b")
    print(prefix + "getting all the numbers")

    number_lines = [infections.text, infection_rate.text, Inzidenz.text, death_cases.text]
    with open('numbers.txt', 'w') as w:
        for line in number_lines:
            w.write(line)
            w.write('\n')
        w.close()
        print(prefix + "numbers written to numbers.txt")

    driver.close()


def generate_image():
    print(prefix + "opening pattern")
    img = Image.open("corona.jpeg")
    width, height = img.size
    draw = ImageDraw.Draw(img)

    font_light = ImageFont.truetype("LibreFranklin-ExtraLight.ttf", 30)
    font_regular = ImageFont.truetype("LibreFranklin-ExtraLight.ttf", 35)
    font_number_regular = ImageFont.truetype("LibreFranklin-ExtraLight.ttf", 45)

    text1 = "Infektionen (gesamt):"
    text3 = "Infektionsrate:"
    text5 = "7-Tage-Inzidenz:"
    text7 = "Todesfälle (gesamt):"

    r = open('numbers.txt', 'r')
    rlines = r.readlines()
    text2 = rlines[0]
    text4 = rlines[1]
    text6 = rlines[2]
    text8 = rlines[3]
    r.close()

    print(prefix + "adding text to image")
    text1_x, text1_y = font_regular.getsize(text1)
    text2_x, text2_y = font_number_regular.getsize(text2)
    text3_x, text3_y = font_regular.getsize(text3)
    text4_x, text4_y = font_number_regular.getsize(text4)
    text5_x, text5_y = font_regular.getsize(text5)
    text6_x, text6_y = font_number_regular.getsize(text6)
    text7_x, text7_y = font_regular.getsize(text7)
    text8_x, text8_y = font_number_regular.getsize(text8)

    draw.text((width - 15 - text1_x, height / 6), text1, (0, 0, 0), font=font_regular)
    draw.text((width + 10 - text2_x, height / 4.5), text2, (0, 0, 0), font=font_number_regular)
    draw.text((width - 15 - text3_x, height / 3), text3, (0, 0, 0), font=font_regular)
    draw.text((width + 10 - text4_x, height / 2.6), text4, (0, 0, 0), font=font_number_regular)
    draw.text((width - 15 - text5_x, height / 2), text5, (0, 0, 0), font=font_regular)
    draw.text((width + 15 - text6_x, height / 2 + 34), text6, (0, 0, 0), font=font_number_regular)
    draw.text((width - 15 - text7_x, height / 2 + 110), text7, (0, 0, 0), font=font_regular)
    draw.text((width + 15 - text8_x, height / 2 + 144), text8, (0, 0, 0), font=font_number_regular)

    draw.text((35, 10), date, (0, 0, 0), font=font_light)
    print(prefix + "saving image to withtext.jpeg")
    img.save("withtext.jpeg")


def login_insta_upload():
    driver = webdriver.Chrome(executable_path='/Users/nicowerner/Documents/Programmieren/python/Corona/chromedriver')
    print(prefix + "Going to instagram.com")
    driver.get("https://www.instagram.com/accounts/login/")
    sleep(1)
    cookies = driver.find_element(By.XPATH, "//button[@class=\"aOOlW  bIiDR  \"]")
    cookies.click()
    print(prefix + "clicked on accept all")
    sleep(4)
    username = driver.find_element(By.XPATH, "//input[@name=\"username\"]")
    username.send_keys(username_file)
    print(prefix + "entered username: " + username_file)
    sleep(1)
    password = driver.find_element(By.XPATH, "//input[@name=\"password\"]")
    password.send_keys(password_file)
    print(prefix + "entered password: " + password_file[:3] + "*****")
    sleep(6)
    info_save = driver.find_element(By.XPATH, "//button[@class=\"sqdOP  L3NKy   y3zKF     \"]")
    info_save.click()
    print(prefix + "pressed login button")
    sleep(4)
    act = driver.find_element(By.XPATH, "//button[@class=\"aOOlW   HoLwm \"]")
    act.click()
    print(prefix + "pressed to not save information")
    sleep(2.5)
    upload_button = driver.find_element(By.XPATH,
                                        "//*[@id=\"react-root\"]/section/nav/div[2]/div/div/div[3]/div/div[3]/div/button")
    upload_button.click()
    sleep(0.5)
    upload = driver.find_element(By.XPATH,
                                 "//input[@accept=\"image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime\"]")
    upload.send_keys('/Users/nicowerner/Documents/Programmieren/python/Corona/withtext.jpeg')
    print(prefix + "uploaded image")
    sleep(3)
    keyboard = Controller()
    for i in range(3):
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        sleep(0.3)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    sleep(0.5)
    for i in range(3):
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        sleep(0.3)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    sleep(0.7)
    password = driver.find_element(By.XPATH, "//textarea[@placeholder=\"Bildunterschrift verfassen …\"]")
    password.send_keys(
        'Die heutigen Corona Zahlen für den ' + date + '. Tragt bitte eine Maske und haltet genügend Abstand.')
    print(prefix + "added description")
    sleep(0.5)
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
    for i in range(7):
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        sleep(0.3)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    sleep(5)


def check_for_new_numbers():
    while True:
        print(prefix + "start searching for new numbers")
        page = requests.get("https://www.corona-in-zahlen.de/landkreise/lk%20ostalbkreis/")
        result = BeautifulSoup(page.content, 'html.parser')

        info = result.find("span", {"class": "badge badge-secondary"}).text
        file = open('date.txt', 'r')
        fline = file.readlines()
        line = fline[0]
        file.close()

        if not line == info:
            print(prefix + "new numbers found!")
            file = open('date.txt', 'w')
            file.write(info)
            file.close()

            get_numbers()
            generate_image()
            login_insta_upload()

        print(prefix + "no new numbers found! going back to sleep for 1 hour")
        sleep(60 * 60)


check_for_new_numbers()
