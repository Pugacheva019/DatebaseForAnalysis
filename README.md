# ParseFromInstagram
This App is a tool for parsing data from Instagram on Python. 
List of Followers and Following in .xlx,      ![](https://portal.iv-edu.ru/dep/mouokinrn/kineshmarn_djachevskaya/DocLib2/Фото/Instagram.jpg)             
time in unix format of all user's post in .xlx,
download video and foto, locations and other information of posts. 

# Install 
Download Python 3.8
Install Pip

      sudo easy_install pip
Install  xlsxwriter, pandas, PyQt5, sys, selenium, requests, BeautifulSoup, os, os.path

      $ pip install XlsxWriter

# Usage


 # Parser followers
This method will give you a list of subscribers.

		followers_count -  number of subscribers
		loops_count -  number of iterations
		followers_ul - raw subscriber name 
		followers_urls - array for subscriber names
		all_urls_div - variable to process followers_ul 
		file - file for recording subscribers

# Parser following
This method will give you a list of subscriptions.

    followers_count -  number of subscriptions
		loops_count -  number of iterations
		followers_ul - raw subscriptions name 
		followers_urls - array for subscriptions names
		all_urls_div - variable to process followers_ul 
		file - file for recording subscriptions

# Parser url post’s 
This method will give you urls of user’s posts

    user_name -  username of the user whose data we collect
    posts_count - post feed
    loops_count - converted posts_count value
    posts_urls - array for urls of post’s
    href -  variable for search and conversion url
    FILE - file for recording urls

# Parser post publication time
This method will give you publication time of posts

    user_name - username of the user whose data we collect
    File - post link file
    post_url - post’s link
    Time -  array for recording the publication time of posts
    FILE - file for recording the publication time of posts
# Parser location of posts
This method will give you location of posts

    user_name - username of the user whose data we collect
    File - post link file
    post_url - post’s link
    LocationData - array for recording the location of posts
    Map - array for recording the placemark on the map 
    url - array for recording the urls of posts
    LocationFile - file for recording the locatioт and placemark on the map of posts

# Parser type of posts
This method will give you type of posts

    user_name - username of the user whose data we collect
    File - post link file
    post_url - post’s link
    f- array for recording the the type of posts
    url - array for recording the urls of posts
    img_src - Xpath for the photo
    video_src -  Xpath for the video
    collection_src -  Xpath for the collection
# Parser post comments
This method will give you comments  of posts

# Downloader publications



