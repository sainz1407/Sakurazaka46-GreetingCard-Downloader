from bs4 import BeautifulSoup as bs
import requests
import urllib.request
import os
import re

def get_html(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
    response = urllib.request.urlopen(req)
    html = response.read()
    return html

def download_image(memName, src_link, savedir):
    if not os.path.isdir(savedir):
        os.makedirs(savedir)

    filename = os.path.join(savedir, memName + '.jpg')
    src_link = re.sub(r'/\d+_\d+_\d+\.jpg$', '.jpg', src_link)
    tmp = requests.get("https://sakurazaka46.com/" + src_link)

    with open(filename, 'wb') as f:
        f.write(tmp.content)

def process_member(memNum):
    url = f"https://sakurazaka46.com/s/s46/artist/{memNum}?ima=0000"
    html = get_html(url)
    res = bs(html, 'html.parser')

    memName = res.find(class_="name").text.strip()
    memPic_src = res.find(class_="ph").find('img')['src']
    memCard_src = res.find(class_="part-card").find('img')['src']
    PHOTO = res.find(class_="part-cimg")

    download_image(memName, memPic_src, "Pic")
    download_image(memName, memCard_src, "GreetingCard")

    if PHOTO:
        photo_src = PHOTO.find('img')['src']
        download_image(memName, photo_src, "GreetingPHOTO")

    print(memName)

memList = ["03", "06", "08", "43", "53", "54", "55", "56", "45", "46", "47", "57", "48", "50", "58", "51", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69"]

for memNum in memList:
    process_member(memNum)
