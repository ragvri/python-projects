import praw
import config
import urllib.request
import os

print(config.username)


# we need an instance of Reddit class to do anything with praw
def logging_in():
    r = praw.Reddit(username=config.username,  # getting username etc for loggin in
                    password=config.password,  # user_agent lets reddit identify who you are
                    client_id=config.client_id,
                    client_secret=config.client_secret,
                    user_agent="rjmessibarca wallpaper getter")

    print("logged in!")
    return r


def get_submissions_url(r):
    subreddit = r.subreddit('EarthPorn')

    list_url = []
    for submissions in subreddit.top(time_filter='day', limit=100):  # gets a list of top 100 url of a day from
        # /r/Earthporn
        list_url.append(submissions.url)
    return list_url


def downloading_image(list):  # we find the first image among the 100 urls which ends with jpg and download that image
    for url in list:
        ending = url[-3:]
        print(ending)
        if ending == 'jpg':
            break

    print(url)
    try:
        req = urllib.request.Request(url=url, headers={'User-Agent': 'Mozilla'})
        resp = urllib.request.urlopen(req)
    except Exception as e:
        print(e)

    CHUNK = 16 * 1024
    with open('1.jpg', 'wb') as f:
        while True:
            chunk = resp.read(CHUNK)
            if not chunk:
                break
            f.write(chunk)


def make_wallpaper():  # set the downloaded image as background
    os.system(
        "gsettings set org.gnome.desktop.background picture-uri "
        "file:///home/raghav/Dropbox/coding/python/projects/reddit_wallpaper_scrapper/1.jpg")
    print('done')


def main():
    r = logging_in()
    l = get_submissions_url(r)
    for i in l:
        print(i)

    downloading_image(l)
    make_wallpaper()


if __name__ == '__main__':
    main()
