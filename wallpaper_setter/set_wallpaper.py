import praw
import config
import urllib.request
import os
import ctypes
import random
import sys
import subprocess

subreddits = {'1': 'AnimeWallpaper', '2': 'ImaginaryLandscapes', '3': 'itookapicture', '4': 'EarthPorn',
              '5': 'wallpaper',
              '6': "wallpapers"}
secure_random = random.SystemRandom()


# we need an instance of Reddit class to do anything with praw
def log_in():
    try:
        reddit = praw.Reddit(
            username=config.username,
            password=config.password,
            client_id=config.client_id,
            client_secret=config.client_secret,
            user_agent=config.user_agent)
    except Exception as e:
        print("Unable to connect\n"+e)
    return reddit


def get_submissions_url(r, sub):
    print("getting link")
    allowed_extensions = ['jpg', 'png', 'bmp']
    subreddit = r.subreddit(sub)

    list_url = []
    for submissions in subreddit.top(time_filter='month',
                                     limit=100):  # gets a list of top 100 url of a day from the subreddit
        if submissions.over_18:  # not nsfw
            continue
        url = submissions.url
        extension = url[-3:]
        if extension in allowed_extensions:
            list_url.append(url)
    return list_url


def download_image(l):  # we find the first image among the 100 urls which ends with jpg and download that image
    print("downloading image")
    url_to_download = secure_random.choice(l)
    file_extension = os.path.splitext(url_to_download)[1]
    try:
        req = urllib.request.Request(url=url_to_download, headers={'User-Agent': 'Mozilla'})
        resp = urllib.request.urlopen(req)
    except Exception as e:
        print(e)

    CHUNK = 1024
    with open('1.jpg', 'wb') as f:
        while True:
            chunk = resp.read(CHUNK)
            if not chunk:
                break
            f.write(chunk)
    return file_extension


def set_wallpaper(file_extension):  # set the downloaded image as background

    location = os.path.dirname(os.path.realpath(__file__))
    file_name = '1' + file_extension
    path = os.path.join(os.path.sep, location, file_name)
    if os.name == 'nt':  # if using windows
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)

    else:  # if using linux
        subprocess.call("gsettings set org.gnome.desktop.background picture-uri file://" + path, shell=True)
    print('done')


def main():
    if len(sys.argv) == 1:
        inp = secure_random.choice(list(subreddits.values()))
    else:
        inp = subreddits[sys.argv[1]]
    reddit = log_in()
    links = get_submissions_url(reddit, inp)

    file_extension = download_image(links)
    set_wallpaper(file_extension)


if __name__ == '__main__':
    main()
