#TODO: make captions saveable

import instaloader

L = instaloader.Instaloader()
username = "nachrichtenleicht"
profile = instaloader.Profile.from_username(L.context, username)

for post in profile.get_posts():
    print(post.caption)
