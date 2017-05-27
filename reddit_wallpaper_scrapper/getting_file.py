import praw
import config
import urllib.request
import os
import ctypes
import random
import sys

wallp = {'1': 'AnimeWallpaper', '2': 'ImaginaryLandscapes', '3': 'itookapicture', '4': 'EarthPorn', '5': 'wallpaper',
         '6': "wallpapers"}
secure_random = random.SystemRandom()


# we need an instance of Reddit class to do anything with praw
def logging_in():
    r = praw.Reddit(
        username=config.username,
        password=config.password,
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent=config.user_agent)

    print("logged in!")
    return r


def get_submissions_url(r, sub):
    endings = ['jpg', 'png', 'bmp']
    subreddit = r.subreddit(sub)

    list_url = []
    for submissions in subreddit.top(time_filter='month',
                                     limit=100):  # gets a list of top 100 url of a day from the subreddit
        if submissions.over_18:  # not nsfw
            continue
        url = submissions.url
        ending = url[-3:]
        if ending in endings:
            list_url.append(url)
    return list_url


def downloading_image(l):  # we find the first image among the 100 urls which ends with jpg and download that image
    url_to_download = secure_random.choice(l)
    formatt = url_to_download[-3:]
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
    return formatt


def make_wallpaper(formatt):  # set the downloaded image as background

    location = os.getcwd()
    if os.name == 'nt':  # if using windows
        print('Windows')
        SPI_SETDESKWALLPAPER = 20
        path = location + "\\1." + formatt
        print(path)
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)

    else:  # if using linux
        path = "file://" + location + "/1.jpg"
        os.system(
            "gsettings set org.gnome.desktop.background picture-uri " + path)
    print('done')


def main():
    if len(sys.argv) == 1:
        inp = secure_random.choice(list(wallp.values()))
    else:
        inp = wallp[sys.argv[1]]
    print(inp)
    r = logging_in()
    l = get_submissions_url(r, inp)

    formatt = downloading_image(l)
    make_wallpaper(formatt)


if __name__ == '__main__':
    main()
