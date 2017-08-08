import praw
import config
import urllib.request
import os
import ctypes
import random
import subprocess
import argparse
from argparse import RawTextHelpFormatter

subreddits = {1: ['AnimeWallpaper', 'Anime'],
              2: ['ImaginaryLandscapes', 'Art', 'ImaginaryBattlefields', 'ImaginaryCityscapes', 'ImaginaryMindscapes',
                  'ImaginaryStarscapes', 'ImaginaryWastelands', 'SpecArt', 'CityPorn'],
              3: ['itookapicture', 'pics'],
              4: ['EarthPorn', 'Earth pics'],
              5: ['wallpaper', 'wallapers'],
              6: ['animals', 'animalporn', 'foxes'],
              7: ["wallpapers", 'wallpapers'],
              8: ['hdsoccer', 'soccer'], }

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
        print("Unable to connect\n" + str(e))
        quit()
    return reddit


def get_submissions_url(r, sub, time_filter='month', isnsfw=False):
    print("getting link")
    print(time_filter)
    allowed_extensions = ['jpg', 'png', 'bmp']
    subreddit = r.subreddit(sub)

    list_url = []
    for submissions in subreddit.top(time_filter=time_filter,
                                     limit=100):  # gets a list of top 100 url of a day from the subreddit
        if not isnsfw and submissions.over_18:  # not nsfw
            continue
        url = submissions.url
        extension = url[-3:]
        if extension in allowed_extensions:
            list_url.append(url)
    return list_url


def download_image(l):  # we find the first image among the 100 urls which ends with jpg and download that image
    print("downloading image")
    url_to_download = secure_random.choice(l)
    file_extension = os.path.splitext(url_to_download)[-1][:4]
    try:
        req = urllib.request.Request(url=url_to_download, headers={'User-Agent': 'Mozilla'})
        resp = urllib.request.urlopen(req)
    except Exception as e:
        print(e)
        quit()

    CHUNK = 1024
    with open('1' + file_extension, 'wb') as f:
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


def parse_input():
    help_for_type = ''
    for key, value in subreddits.items():
        text = str(key) + ' for ' + value[1]
        help_for_type += text
        help_for_type += '\n'
    help_for_time = "'hour' to get top posts of last hour \n'day' to get top posts of today\n'month' to get top posts " \
                    "of past month\n'year' to get top posts of last year\n'all' to get all time top posts\n"
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('--time', type=str, default='month', help=help_for_time)
    parser.add_argument('--type', type=int, default=None, help=help_for_type)
    parser.add_argument('--nsfw', type=str, default=False, help="type True to get nsfw wallpapers")
    parser.add_argument('--subreddit', default=None, type=str, help="Type subreddit name to download wallpaper from")
    args = parser.parse_args()
    return args


def main():
    args = parse_input()
    if args.subreddit is not None:
        subreddit = args.subreddit
    elif args.type is None:
        subreddit_list = secure_random.choice(list(subreddits.values()))
        subreddit = subreddit_list[random.randint(0, len(subreddit_list)) - 1]
    else:
        subreddit_list = subreddits[args.type]
        subreddit = subreddit_list[random.randint(0, len(subreddit_list) - 1)]
    reddit = log_in()
    print(subreddit)
    links = get_submissions_url(reddit, subreddit, time_filter=args.time, isnsfw=args.nsfw)

    file_extension = download_image(links)
    set_wallpaper(file_extension)


if __name__ == '__main__':
    main()
