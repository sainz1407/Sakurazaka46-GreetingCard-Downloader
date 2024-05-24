from bs4 import BeautifulSoup as bs
import requests
import urllib.request
import os
import io
import sys
import warnings
import json
import re
warnings.filterwarnings("ignore")

def get_html(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
    response = urllib.request.urlopen(req)
    html = response.read()
    return html

def downloadImg(memName, srcLink, savedir):
    if not os.path.isdir(savedir):
        os.makedirs(savedir)
    tmp = requests.get(srcLink)
    with open(os.path.join(savedir, memName + '.jpg'), 'wb') as f:
        f.write(tmp.content)
    return "OK"

memList = ["03", "06", "08", "43", "53", "54", "55", "56", "45", "46", "47", "57", "48", "50", "58", "51", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69"]

for memNum in memList:
    url = "https://sakurazaka46.com/s/s46/artist/" + str(memNum) + "?ima=0000"
    html = get_html(url)
    res = bs(html, 'html.parser')
    memPic = "https://sakurazaka46.com/" + res.find(class_="ph").find('img')['src']
    memName = res.find(class_="name").text.strip()
    PHOTO = res.find(class_="part-cimg")
    memCard_img_tag = res.find(class_="part-card").find('img')
    memCard_src = memCard_img_tag['src']

    memCard_src = re.sub(r'/\d+_\d+_\d+\.jpg$', '.jpg', memCard_src)
    memCard = "https://sakurazaka46.com/" + memCard_src
    if PHOTO is None:
        downloadImg(memName, memPic, "Pic")
        downloadImg(memName, memCard, "GreetingCard")
    else:
        photo_img_tag = PHOTO.find('img')
        photo_src = photo_img_tag['src']
        photo_src = re.sub(r'/\d+_\d+_\d+\.jpg$', '.jpg', photo_src)
        Photo = "https://sakurazaka46.com/" + photo_src
        downloadImg(memName, memPic, "Pic")
        downloadImg(memName, memCard, "GreetingCard")
        downloadImg(memName, Photo, "GreetingPHOTO")
    print(memName)