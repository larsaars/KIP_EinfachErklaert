#TODO: make captions saveable

import instaloader
import datahandler.DataHandler as DataHandler

L = instaloader.Instaloader()
username = "nachrichtenleicht"
profile = instaloader.Profile.from_username(L.context, username)

dh = DataHandler.DataHandler('dlf')


def metadata_dict(post: instaloader.Post) -> dict:
    return {
        "url": post.url,
        "title": post.caption.split()[:7] if post.title is None else post.title,
        "kicker": "",
        "date": post.date_utc.strftime("%Y-%m-%d"),
        "description": "",
        "image_description": "",
        "image_url": ""
    }


for post in profile.get_posts():
    # dh.save_article("easy", metadata_dict(post), post.caption, "", download_audio=False)
    print(metadata_dict(post))