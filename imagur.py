from imgurpython import ImgurClient
import json
import pprint as pp
import random
import os

imagur_id = os.environ.get('imgur_id')
imagur_secret = os.environ.get('imgur_secret')

imagur = ImgurClient(
    client_id=str(imagur_id),
    client_secret=str(imagur_secret)
    )

def defmemes():
    result = imagur.default_memes()

    meme_list = result

    chose = random.choices(meme_list)

    for res in chose:
        return res.link

def imgrandom():
    result = imagur.gallery_random()

    image_list = result

    chose = random.choices(image_list)

    for res in chose:
        return res.link

def memes():
    result = imagur.memes_subgallery()

    meme_list = result

    chose = random.choices(meme_list)

    for res in chose:
        return res.link

def images(items : str):
    result = imagur.gallery_search(q=items)

    image_list = result

    chose = random.choices(image_list)

    for res in chose:
        return res.link

def subreddit(subreddit_name : str):
    result = imagur.subreddit_gallery(subreddit=subreddit_name)

    image_list = result

    chose = random.choices(image_list)

    for res in chose:
        return res.link