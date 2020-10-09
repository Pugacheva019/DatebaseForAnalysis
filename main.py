from selenium import webdriver
import time
import os
import requests
import xlwt
import pandas
import os.path
import tkinter
from tkinter import *

browser = webdriver.Chrome("...")


# метод входа в инстаграмм
def SingInInstagram():
    browser.get("https://www.instagram.com/accounts/login")
    time.sleep(5)
    browser.find_element_by_xpath("/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div/div["
                                  "1]/div/label/input").send_keys("login")
    browser.find_element_by_xpath("/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div/div["
                                  "2]/div/label/input").send_keys("passport")
    browser.find_element_by_xpath("/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div/div[3]").click()
    time.sleep(4)
    return 0


# метод составление списка подписчиков
def GetFollowers(user_name):
    browser.get("https://www.instagram.com/" + user_name)
    time.sleep(4)
    file_name = user_name
    if os.path.exists(f"{file_name}"):  # создаем папку пользователя
        print("Папка уже существует!")
    else:
        os.mkdir(file_name)

    print(f"Пользователь {file_name} успешно найден, начинаем скачивать логины подписчиков!")
    time.sleep(2)
    followers_button = browser.find_element_by_xpath(
        "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a")
    followers_count = followers_button.text
    if 'млн' in followers_count:
        count = ''
        for i in range(0, len(followers_count)):
            if followers_count[i] in 'млнподписчиков':
                count = count
            else:
                count += followers_count[i]
            print(count)
        followers_count = int(count) * 1000000
        print(followers_count)
    elif 'тыс' in followers_count:
        count = ''
        for i in range(0, len(followers_count)):
            if followers_count[i] in 'тысподписчиков':
                count = count
            else:
                count += followers_count[i]
        followers_count = int(count) * 1000
    else:
        followers_count = int(followers_count.split(' ')[0])
    print(f"Количество подписчиков: {followers_count}")
    time.sleep(2)
    if int(followers_count / 12) > 10:
        loops_count = 10
    else:
        loops_count = int(followers_count / 12)
    print(f"Число итераций: {loops_count}")
    time.sleep(4)
    followers_button.click()
    time.sleep(4)
    followers_ul = browser.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")

    followers_urls = []
    for i in range(0, loops_count):
        browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
        time.sleep(4)
        print(f"Итерация #{i}")

    all_urls_div = followers_ul.find_elements_by_tag_name("li")

    for url in all_urls_div:
        url = url.find_element_by_tag_name("a").get_attribute("href")
        followers_urls.append(url)

    # сохраняем всех подписчиков пользователя в файл
    file = xlwt.Workbook(f"{file_name}/{file_name}followers.xls", "rb")
    FiLESheet = file.add_sheet('followers')
    file.save(f"{file_name}/{file_name}followers.xls")
    FiLESheet.write(0, 0, user_name)
    i = 1
    print(followers_urls)
    for link in followers_urls:
        link = link[26:len(link) - 1]
        FiLESheet.write(0, i, link)
        i += 1
    file.save(f"{file_name}/{file_name}followers.xls")
    return followers_count


def GetFollowing(user_name):
    browser.get("https://www.instagram.com/" + user_name)
    time.sleep(4)
    file_name = user_name
    if os.path.exists(f"{file_name}"):  # создаем папку пользователя
        print("Папка уже существует!")
    else:
        os.mkdir(file_name)

    print(f"Пользователь {file_name} успешно найден, начинаем скачивать логины подписчиков!")
    time.sleep(2)
    following_button = browser.find_element_by_xpath(
        "/html/body/div[1]/section/main/div/ul/li[3]/a")
    following_count = following_button.text
    following_count = int(following_count.split(' ')[0])
    print(f"Количество подписок: {following_count}")
    time.sleep(2)

    loops_count = int(following_count / 12)
    print(f"Число итераций: {loops_count}")
    time.sleep(4)
    following_button.click()
    time.sleep(4)
    following_ul = browser.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")

    followers_urls = []
    for i in range(0, loops_count):
        browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", following_ul)
        time.sleep(4)
        print(f"Итерация #{i}")

    all_urls_div = following_ul.find_elements_by_tag_name("li")

    for url in all_urls_div:
        url = url.find_element_by_tag_name("a").get_attribute("href")
        followers_urls.append(url)

    # сохраняем всех подписок пользователя в файл
    with open(f"{file_name}/{file_name}_following.txt", "a") as FILE:
        for link in followers_urls:
            FILE.write(link[26:len(link) - 1] + "\n")


# метод собирания ссылок на посты пользователя
def PutPosts(user_name):
    file_name = user_name
    if os.path.exists(f"{file_name}"):  # создаем папку пользователя
        print("Папка уже существует!")
    else:
        os.mkdir(file_name)
    browser.get("https://www.instagram.com/" + user_name)
    time.sleep(4)
    print("Пользователь успешно найден" + user_name)
    time.sleep(2)
    posts_count = str(browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li["
                                                    "1]/span/span").text)
    if posts_count.find(" ") != -1:
        print(posts_count)
        new_posts_count = ""
        for i in range(0, len(posts_count)):
            if posts_count[i] != " ":
                new_posts_count += posts_count[i]
        posts_count = new_posts_count
        print(posts_count)
    posts_count = int(posts_count)
    if posts_count > 3:
        loops_count = 3
    else:
        loops_count = int(posts_count)
    print(loops_count)
    posts_urls = []
    for i in range(0, loops_count):
        hrefs = browser.find_elements_by_tag_name('a')
        hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

        for href in hrefs:
            posts_urls.append(href)

        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        print(f"Итерация #{i}")

    file_name = user_name

    with open(f'{file_name}/{file_name}_posts.txt', 'a') as FILE:
        for post_url in posts_urls:
            FILE.write(post_url + "\n")
    set_posts_urls = set(posts_urls)
    set_posts_urls = list(set_posts_urls)


# метод скачивания публикаций
def DownLoaderFile(user_name):
    PutPosts(user_name)
    file_name = user_name
    time.sleep(4)
    browser.get("https://www.instagram.com/" + user_name)
    time.sleep(4)
    if os.path.exists(f"{file_name}"):  # создаём папку с именем пользователя
        print("Папка уже существует!")
        return
    else:
        os.mkdir(file_name)
    img_and_video_src_urls = []
    with open(f'{file_name}/{file_name}.txt') as file:
        urls_list = file.readlines()

        for post_url in urls_list:
            try:
                browser.get(post_url)
                time.sleep(4)

                img_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/img"
                video_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/div/div/video"
                post_id = post_url.split("/")[-2]

                if browser.find_element_by_xpath(img_src):
                    img_src_url = browser.find_element_by_xpath(img_src).get_attribute("src")
                    img_and_video_src_urls.append(img_src_url)

                    # сохраняем изображение
                    get_img = requests.get(img_src_url)
                    with open(f"{file_name}/{file_name}_{post_id}_img.jpg", "wb") as img_file:
                        img_file.write(get_img.content)

                elif browser.find_element_by_xpath(video_src):
                    video_src_url = browser.find_element_by_xpath(video_src).get_attribute("src")
                    img_and_video_src_urls.append(video_src_url)

                    # сохраняем видео
                    get_video = requests.get(video_src_url, stream=True)
                    with open(f"{file_name}/{file_name}_{post_id}_video.mp4", "wb") as video_file:
                        for chunk in get_video.iter_content(chunk_size=1024 * 1024):
                            if chunk:
                                video_file.write(chunk)
                else:
                    # print("Упс! Что-то пошло не так!")
                    img_and_video_src_urls.append(f"{post_url}, нет ссылки!")
                print(f"Контент из поста {post_url} успешно скачан!")

            except Exception as ex:
                print(ex)


# метод парсинга времени
def TimeOfPost(name, number):
    file_name = name
    File = open(f'{file_name}/{file_name}_posts.txt', 'r')
    Time = []
    for post_url in File:
        browser.get(post_url)
        g = browser.find_element_by_xpath("//time").get_attribute("datetime")
        Time.append(g)
    print(Time)
    T = 1
    FILE = xlwt.Workbook(f"{file_name}/{file_name}timeOfPost.xls", "rb")
    FiLESheet = FILE.add_sheet('time')
    FILE.save(f"{file_name}/{file_name}timeOfPost.xls")
    FiLESheet.write(number, 0, name)
    for date in Time:
        date = date[0:10] + " " + date[11:19]
        date = int(time.mktime(time.strptime('2000-01-01 12:34:00', '%Y-%m-%d %H:%M:%S')))
        FiLESheet.write(number, T, date)
        T += 1
    FILE.save(f"{file_name}/{file_name}timeOfPost.xls")


'''
SingInInstagram()
username = "natgeo"
t = 0
TimeOfPost(username, t)
Followers = pandas.read_excel(f"{username}/{username}followers1.xls", 'followers')
List = Followers.columns.ravel()
TimePost = pandas.read_excel(f"{username}/{username}timeOfPost.xls", 'time')
Timing = TimePost.columns.ravel()
for f in List:
    print(f)
    if f != username:
        PutPosts(f)
        TimeOfPost(f, t)
    t += 1
    TimePost = pandas.read_excel(f"{f}/{f}timeOfPost.xls", 'time')
browser.close()
'''
'''
username = "natgeo"
t = 0
i = 0
Followers = pandas.read_excel(f"{username}/{username}followers.xls", 'followers')
List = Followers.columns.ravel()
FILE = xlwt.Workbook(f"timeOfPost.xls", "wb")
FILE_Sheet = FILE.add_sheet('time')
for username in List:
    TimePost = pandas.read_excel(f"{username}/{username}timeOfPost.xls", 'time')
    Timing = TimePost.columns.ravel()
    for data in Timing:
        FILE_Sheet.write(i, t, data)
        i += 1
    t += 1
'''
root = Tk()
root.title("GUI на Python")
root.geometry("300x250")
