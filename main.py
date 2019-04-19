from PIL import Image
from bs4 import BeautifulSoup
import os
import requests

if not os.path.exists(os.path.abspath('pages/')):
    os.mkdir(os.path.abspath('pages/'))

if not os.path.exists(os.path.abspath('frames/')):
    os.mkdir(os.path.abspath('frames/'))

now_pages = 300

for i in range(2, now_pages + 1):
    url = 'http://skyboxcomic.com/'
    url_comics = 'http://skyboxcomic.com/comics/'

    path = os.path.abspath('pages/' + str(i) + '.jpg')

    print('Viewing:', i)

    if not os.path.exists(path):  # don't download if we have already page
        url_r = requests.get(url_comics + str(i))
        bs = BeautifulSoup(url_r.content)
        print('Downloading:', i, url + bs.find_all('img', {'id': 'comicimage'})[0]['src'])  # human readable
        r = requests.get(url + bs.find_all('img', {'id': 'comicimage'})[0]['src'], stream=True)  # get file stream
        with open(path, 'wb') as f:  # copy paste from stackoverflow, download file
            for chunk in r.iter_content(chunk_size=2048):
                if chunk:
                    f.write(chunk)
                else:
                    print(chunk)

num = 0

for j in range(2, now_pages + 1):
    image = '{}.jpg'.format(j)
    im = Image.open(os.path.abspath('pages/' + image))
    count = im.size[1] // 338

    # frames = []  # for gifs

    print('Working page:', image, 'Frames done:', num)

    for i in range(count):
        frame_path = os.path.abspath('frames/' + str(num) + '.jpg')
        if not os.path.exists(frame_path):
            box = (0, i * 338, im.size[0], (i + 1) * 338)
            region = im.crop(box)
            region = region.resize((region.size[0], region.size[1]))
            region.save(frame_path, quality=90)
        num += 1
        # region = region.convert(mode='P', palette=Image.ADAPTIVE)  # for gifs
        # frames.append(region)  # for gifs

    # frames[0].save('animation.gif', append_images=frames[1:], save_all=True, duration=250, loop=0)  # for gifs

