from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import os
import requests
import xlwt
import pandas
import pandas as pd
import os.path
from PyQt5 import QtWidgets
import sys
from DataSet import Ui_Dialog
from bs4 import BeautifulSoup as bs

# front-end
app = QtWidgets.QApplication(sys.argv)
Dialog = QtWidgets.QDialog()
ui: Ui_Dialog = Ui_Dialog()
ui.setupUi(Dialog)
Dialog.show()


# метод входа в инстаграмм
def SingInInstagram(browser):
    browser.get("https://www.instagram.com/accounts/login")
    time.sleep(3)
    browser.find_element_by_xpath("/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div/div["
                                  "1]/div/label/input").send_keys("knowlenge")
    browser.find_element_by_xpath("/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div/div["
                                  "2]/div/label/input").send_keys("Anita2001")
    browser.find_element_by_xpath("/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div/div[3]").click()
    time.sleep(2)


# метод составление списка подписчиков
def GetFollowers(user_name):
    options = webdriver.ChromeOptions()
    options.set_headless(True)
    browser = webdriver.Chrome("/Users/anna/PycharmProjects/DataSet/chromedriver")
    SingInInstagram(browser)
    time.sleep(2)
    browser.get("https://www.instagram.com/" + user_name)
    time.sleep(4)
    file_name = user_name
    if os.path.exists(f"{file_name}"):  # создаем папку пользователя
        print("Папка уже существует!")
    else:
        os.mkdir(file_name)
    print(f"Пользователь {file_name} успешно найден, начинаем скачивать логины подписчиков!")
    time.sleep(2)
    followers_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a")
    followers_count = followers_button.text
    if 'млн' in followers_count:
        count = ''
        for i in range(0, len(followers_count)):
            if followers_count[i] in 'млнподписчиков':
                break
            else:
                count += followers_count[i]
            print(count)
        followers_count = int(count) * 1000000
        print(followers_count)
    elif 'тыс' in followers_count:
        count = ''
        for i in range(0, len(followers_count)):
            if followers_count[i] in 'тысподписчиков':
                break
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
    followers_ul = browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
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
    options = webdriver.ChromeOptions()
    options.set_headless(True)
    browser = webdriver.Chrome("/Users/anna/PycharmProjects/DataSet/chromedriver")
    SingInInstagram(browser)
    time.sleep(5)
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


def PutPostsSet(user_name, browser):
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
    if posts_count > 12:
        loops_count = 12
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


# метод собирания ссылок на посты пользователя
def PutPosts(user_name):
    options = webdriver.ChromeOptions()
    options.set_headless(True)
    browser = webdriver.Chrome("/Users/anna/PycharmProjects/DataSet/chromedriver")
    SingInInstagram(browser)
    time.sleep(5)
    file_name = user_name
    if os.path.exists(f"{file_name}"):  # создаем папку пользователя
        print("Папка уже существует!")
        if os.path.exists(f'{file_name}/{file_name}_posts.txt'):
            return
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
    if posts_count > 10:
        loops_count = 10
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
    df = pd.DataFrame(posts_urls)
    df.to_excel(f'{file_name}/{file_name}.xls')


# метод скачивания публикаций
def DownLoaderFile(user_name):
    options = webdriver.ChromeOptions()
    options.set_headless(True)
    browser = webdriver.Chrome("/Users/anna/PycharmProjects/DataSet/chromedriver", options=options)
    SingInInstagram(browser)
    PutPostsSet(user_name, browser)
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
    with open(f'{file_name}/{file_name}_posts.txt') as file:
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

            except NoSuchElementException:
                img_and_video_src_urls.append(f"{post_url}, нет ссылки!")


# метод парсинга времени
def TimeOfPost(user_name):
    options = webdriver.ChromeOptions()
    options.set_headless(True)
    browser = webdriver.Chrome("/Users/anna/PycharmProjects/DataSet/chromedriver")
    SingInInstagram(browser)
    time.sleep(2)
    file_name = user_name
    if os.path.exists(f'{file_name}/{file_name}_posts.txt'):
        File = open(f'{file_name}/{file_name}_posts.txt', 'r')
    else:
        print("here")
        PutPostsSet(user_name, browser)
        File = open(f'{file_name}/{file_name}_posts.txt', 'r')
    if os.path.exists(f'{file_name}/{file_name}timeOfPost.xls'):
        return
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
    FiLESheet.write(0, 0, user_name)
    for date in Time:
        date = date[0:10] + " " + date[11:19]
        date = int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')))
        FiLESheet.write(0, T, date)
        T += 1
    FILE.save(f"{file_name}/{file_name}timeOfPost.xls")
    browser.close()


def Comment(user_name):
    print("comm")
    options = webdriver.ChromeOptions()
    options.set_headless(True)
    browser = webdriver.Chrome("/Users/anna/PycharmProjects/DataSet/chromedriver", options=options)
    file_name = user_name
    if os.path.exists(f'{file_name}/{file_name}_posts.txt'):
        print("file here")
    else:
        PutPostsSet(user_name, browser)
    File = open(f'{file_name}/{file_name}_posts.txt', 'r')
    AllComments = []
    url = []
    for post_url in File:
        url.append(post_url)
        CommentsPost = []
        browser.get(post_url)
        browser.implicitly_wait(5)
        while browser.find_elements_by_xpath('//span[@aria-label="Load more comments"]'):
            button = browser.find_element_by_xpath('//span[@aria-label="Load more comments"]')
            button.click()
            browser.implicitly_wait(10)
        post_url = browser.page_source
        soup = bs(post_url, 'html.parser')
        comments = soup.find_all('li', {'class': 'gElp9'})
        for i in range(len(comments)):
            res = comments[i]
            txt = res.find("span").text
            CommentsPost.append(txt)
        if len(CommentsPost) == 0:
            CommentsPost.append('-')
        AllComments.append(CommentsPost)
        print(CommentsPost)
    Comments = pd.DataFrame(AllComments)
    time.sleep(1)
    Comments['post'] = url
    Comments.to_excel(f"{file_name}/{file_name}comment.xls", user_name)
    browser.close()


def Location(user_name):
    options = webdriver.ChromeOptions()
    options.set_headless(True)
    browser = webdriver.Chrome("/Users/anna/PycharmProjects/DataSet/chromedriver", options=options)
    file_name = user_name
    if os.path.exists(f'{file_name}/{file_name}_posts.txt'):
        print("file here")
    else:
        PutPostsSet(user_name, browser)
    File = open(f'{file_name}/{file_name}_posts.txt', 'r')
    LocationData = []
    url = []
    Map = []
    for post_url in File:
        browser.get(post_url)
        url.append(post_url)
        locationPath = "/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[2]/div[2]/a"
        try:
            g = browser.find_element_by_xpath(locationPath).get_attribute("href")
            Map.append(g)
            stroka = browser.find_element_by_xpath(locationPath).text
            LocationData.append(stroka)
        except NoSuchElementException:
            LocationData.append("not information")
            Map.append("not information")
    LocationFile = pd.DataFrame(LocationData)
    time.sleep(1)
    print(Map)
    LocationFile['map'] = Map
    LocationFile['post'] = url
    LocationFile.to_excel(f"{file_name}/{file_name}location.xls", user_name)
    browser.close()


def xpath_exists(browser, url):
    try:
        browser.find_element_by_xpath(url)
        exist = True
    except NoSuchElementException:
        exist = False
    return exist


def Format(user_name):
    options = webdriver.ChromeOptions()
    options.set_headless(True)
    browser = webdriver.Chrome("/Users/anna/PycharmProjects/DataSet/chromedriver")
    file_name = user_name
    if os.path.exists(f'{file_name}/{file_name}_posts.txt'):
        print("file here")
    else:
        PutPostsSet(user_name, browser)
    File = open(f'{file_name}/{file_name}_posts.txt', 'r')
    url = []
    f = []
    for post_url in File:
        try:
            url.append(post_url)
            browser.get(post_url)
            time.sleep(4)
            img_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/img"
            video_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/div/div/video"
            collection_src = "/html/body/div[1]/section/main/div/div/article/div[2]/div/div[1]/div[2]/div/button/div"
            post_id = post_url.split("/")[-2]
            photo = "photo"
            video = "video"
            if xpath_exists(browser, img_src):
                f.append(photo)
                print(photo)
            elif xpath_exists(browser, video_src):
                f.append(video)
                print(video)
            elif xpath_exists(browser, collection_src):
                f.append("коллекция")
            else:
                f.append("фото или видео с отметкой")
        except NoSuchElementException:
            f.append("not information")
    fpd = pd.DataFrame(f)
    fpd['posts'] = url
    fpd.to_excel(f"{file_name}/{file_name}format.xls", user_name)


def DateSet():
    user_name = ui.textEdit.toPlainText()
    options = webdriver.ChromeOptions()
    options.set_headless(True)
    browser = webdriver.Chrome("/Users/anna/PycharmProjects/DataSet/chromedriver")
    SingInInstagram(browser)
    if os.path.exists(f"{user_name}/{user_name}followers.xls"):
        Followers = pandas.read_excel(f"{user_name}/{user_name}followers.xls", 'followers')
    else:
        GetFollowers(user_name)
        Followers = pandas.read_excel(f"{user_name}/{user_name}followers.xls", 'followers')
    List = Followers.columns.ravel()
    for f in List:
        if ui.checkBoxUrl.isChecked():
            PutPostsSet(f, browser)
        if ui.checkBoxTime.isChecked():
            if os.path.exists(f"{f}/{f}_posts.txt"):
                TimeOfPost(f)
            else:
                PutPostsSet(f, browser)
        if ui.checkBoxDownload.isChecked():
            if os.path.exists(f"{f}/{f}_posts.txt"):
                DownLoaderFile(f)
            else:
                PutPostsSet(f, browser)
                DownLoaderFile(f)
        if ui.CommentBox.isChecked():
            if os.path.exists(f"{f}/{f}_posts.txt"):
                Comment(f)
            else:
                PutPostsSet(f, browser)
                Comment(f)
        if ui.TagBox.isChecked():
            if os.path.exists(f"{f}/{f}_posts.txt"):
                Location(f)
            else:
                PutPostsSet(f, browser)
                Location(f)
    browser.close()
    data(user_name)


def DataSetButton():
    user_name = ui.textEdit.toPlainText()
    if ui.checkBoxDataSet.isChecked():
        DateSet()
    else:
        if ui.CheckBoxFollowers.isChecked():
            print("followers")
            GetFollowers(user_name)
        if ui.checkBoxUrl.isChecked():
            print("posts")
            PutPosts(user_name)
        if ui.checkBoxTime.isChecked():
            print("time")
            TimeOfPost(user_name)
        if ui.checkBoxDownload.isChecked():
            DownLoaderFile(user_name)
        if ui.CommentBox.isChecked():
            Comment(user_name)
        if ui.TagBox_2.isChecked():
            Location(user_name)
        if ui.CheckBoxFollowers_2.isChecked():
            GetFollowing(user_name)
        if ui.TagBox_3.isChecked():
            Format(user_name)


def data(user):
    Followers = pandas.read_excel(f"{user}/{user}followers.xls", 'followers')
    List = Followers.columns.ravel()
    Information = []
    for f in List:
        if os.path.exists(f"{f}/{f}_posts.txt"):
            if os.path.exists(f"{f}/{f}timeOfPost.xls"):
                Time = pandas.read_excel(f"{f}/{f}timeOfPost.xls", 'time')
                Time = Time.columns.ravel()
                Information.append(Time)
            else:
                TimeOfPost(f)
                Time = pandas.read_excel(f"{f}/{f}timeOfPost.xls", 'time')
                Time = Time.columns.ravel()
                Information.append(Time)
        else:
            PutPosts(f)
            TimeOfPost(f)
            Time = pandas.read_excel(f"{f}/{f}timeOfPost.xls", 'time')
            Time = Time.columns.ravel()
            Information.append(Time)
    df = pd.DataFrame(Information)
    df.to_excel("TimeOfPosts.xls")


# front-end
ui.DataSetButton_2.clicked.connect(DataSetButton)
ui.DataSetButton_2.show()
app.exec_()
