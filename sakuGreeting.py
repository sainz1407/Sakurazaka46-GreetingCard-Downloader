from bs4 import BeautifulSoup as bs
import requests
import urllib.request
import os
import re

def get_html(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
    response = urllib.request.urlopen(req)
    return response.read()

def get_member_list():
    search_url = "https://www.hinatazaka46.com/s/official/search/artist?ima=0000"
    html = get_html(search_url)
    res = bs(html, 'html.parser')
    member_list = []
    sorted_div = res.find('div', class_='sorted sort-default current')
    if sorted_div:
        member_items = sorted_div.find_all('li', class_='p-member__item')
        for item in member_items:
            data_member = item.get('data-member')
            if data_member:
                member_list.append(data_member)
    return member_list

def download_image(memName, src_link, savedir):
    if not os.path.isdir(savedir):
        os.makedirs(savedir)
    filename = os.path.join(savedir, memNum + "." + memName + '.jpg')
    src_link = re.sub(r'/\d+_\d+_\d+\.jpg$', '.jpg', src_link)
    with open(filename, 'wb') as f:
        f.write(requests.get(src_link).content)

def process_member(memNum):
    url = f"https://hinatazaka46.com/s/official/artist/{memNum}?ima=0000"
    html = get_html(url)
    res = bs(html, 'html.parser')

    memName = res.find(class_="c-member__name--info").text.strip()
    memPic_src = res.find(class_="c-member__thumb__large").find('img')['src']

    memCard_div = res.find(class_="gimg_wrap sub")
    memCard_src = memCard_div.find('img', {'data-eventcategory': 'メンバー'})['src'] if memCard_div else None

    PHOTO_div = res.find('button', {'type': 'subbmit'})
    photo_src = PHOTO_div.find('div', class_="gimg_wrap").find('img')['src'] if PHOTO_div else None

    download_image(memName, memPic_src, "Pic")
    if memCard_src:
        download_image(memName, memCard_src, "GreetingCard")
    if photo_src:
        download_image(memName, photo_src, "GreetingPHOTO")
    print(memName)

memList = get_member_list()
for memNum in memList:
    process_member(memNum)
