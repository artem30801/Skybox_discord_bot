from PIL import Image
from bs4 import BeautifulSoup
import requests

import os
import asyncio

from functools import partial
import aiofiles


def process_page(im, i):
    box = (0, i * 338, im.size[0], (i + 1) * 338)
    region = im.crop(box)
    return region.resize((region.size[0], region.size[1]))


def save_frame(region, path):
    region.save(path, quality=90)


def process_gif(region):
    return region.convert(mode='P', palette=Image.ADAPTIVE)


def save_gif(frames, path):
    frames[0].save(path, append_images=frames[1:], save_all=True, duration=350, loop=0)


async def pull_comic(now_pages=300, pages_dir='pages/', frames_dir='frames/', gif_dir='gif/'):
    try:
        loop = asyncio.get_running_loop()
    except AttributeError:
        loop = asyncio.get_event_loop()

    if not os.path.exists(os.path.abspath(pages_dir)):
        os.mkdir(os.path.abspath(pages_dir))

    if not os.path.exists(os.path.abspath(frames_dir)):
        os.mkdir(os.path.abspath(frames_dir))

    if not os.path.exists(os.path.abspath(gif_dir)):
        os.mkdir(os.path.abspath(gif_dir))

    url = 'http://skyboxcomic.com/'
    url_comics = 'http://skyboxcomic.com/comics/'
    for i in range(2, now_pages + 1):

        path = os.path.abspath(pages_dir + str(i) + '.jpg')

        print('Viewing:', i)

        if not os.path.exists(path):  # don't download if we have already page
            url_r = requests.get(url_comics + str(i))
            bs = BeautifulSoup(url_r.content)
            print('Downloading:', i, url + bs.find_all('img', {'id': 'comicimage'})[0]['src'])  # human readable
            r = requests.get(url + bs.find_all('img', {'id': 'comicimage'})[0]['src'], stream=True)  # get file stream
            async with aiofiles.open(path, 'wb') as f:  # copy paste from stackoverflow, download file
                for chunk in r.iter_content(chunk_size=2048):
                    if chunk:
                        await f.write(chunk)
                    else:
                        print(chunk)

    num = 0
    added_frames = 0
    added_gifs = 0

    for j in range(2, now_pages + 1):
        image = '{}.jpg'.format(j)
        im = Image.open(os.path.abspath(pages_dir + image))
        count = im.size[1] // 338

        frames = []  # for gifs

        print('Splitting page:', image, 'Frames done:', num)
        gif_path = os.path.abspath(gif_dir+str(j)+'.gif')

        for i in range(count):
            frame_path = os.path.abspath(frames_dir + str(num) + '.jpg')
            if (not os.path.exists(gif_path)) or (not os.path.exists(frame_path)):

                region = await loop.run_in_executor(None, partial(process_page, im, i))

                if not os.path.exists(frame_path):
                    await loop.run_in_executor(None, partial(save_frame, region, frame_path))
                    added_frames += 1

                if not os.path.exists(gif_path):
                    region = await loop.run_in_executor(None, partial(process_gif, region))
                    frames.append(region)  # for gifs
            num += 1

        if not os.path.exists(gif_path):
            await loop.run_in_executor(None, partial(save_gif, frames, gif_path))
            added_gifs += 1
    return added_frames, added_gifs
