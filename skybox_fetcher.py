from PIL import Image
from bs4 import BeautifulSoup
import requests

import os
import re
import pickle
import asyncio
import statistics

from functools import partial
import aiofiles
import collections

url = 'http://skybox.thecomicseries.com/'
url_comics = 'comics/'
user_votes_file = 'votes.txt'


def process_page(im, i):
    box = (0, i * 338, im.size[0], (i + 1) * 338)
    region = im.crop(box)
    return region.resize((region.size[0], region.size[1]))


def save_frame(region, path):
    region.save(path, quality=90)


def process_gif(region):
    return region.convert(mode='P', palette=Image.ADAPTIVE)


def save_gif(frames, path, timing=None):
    if timing is None:
        timing = [1000]
    if len(timing) == 1:
        timing = timing[0]
    frames[0].save(path, append_images=frames[1:], save_all=True, duration=timing, loop=0)


def get_last_page():
    url_r = requests.get(url+url_comics)
    bs = BeautifulSoup(url_r.content, features="html.parser")
    last = bs.find('div', {'class': 'title'}).get_text().split()[1]
    return int(last)


def get_arcs_names_list():
    url_r = requests.get(url+'archive/')
    bs = BeautifulSoup(url_r.content, features="html.parser")
    st = bs.find_all('div', {'class': 'subtitle'})

    arcs_list = []
    for name in st:
        arcs_list.append(name.get_text())

    arcs_list[0] = "IM Break"
    return arcs_list


async def pull_comic(pages_dir='pages/', frames_dir='frames/', gif_dir='gif/', databse='database.txt'):
    if not os.path.exists(os.path.abspath(pages_dir)):
        os.mkdir(os.path.abspath(pages_dir))

    now_pages = get_last_page()
    print("Found {} comic pages".format(now_pages))

    arcs = get_arcs_names_list()

    if os.path.exists(os.path.abspath(databse)):
        with open(os.path.abspath(databse), 'rb') as f:
            _, data = pickle.load(f)
            print("Loaded from file. {}".format(data))
    else:
        data = collections.OrderedDict()

    for page_number in range(2, now_pages + 1):
        print('Viewing:', page_number)
        path = os.path.abspath(pages_dir + str(page_number) + '.jpg')

        if not os.path.exists(path):  # don't download if we have already page
            url_r = requests.get(url + url_comics + str(page_number))
            bs = BeautifulSoup(url_r.content, features="html.parser")

            titles = re.split('\s|-', bs.find('div', {'class': 'title'}).get_text())[3:]
            titles = list(filter(None, titles))
            if titles[0] == 'Arc':
                data[arcs[int(titles[1])], titles[2]] = (0, 0)
            elif titles[0] == 'IM':
                data[arcs[0], titles[2]] = (0, 0)

            img_link = bs.find_all('img', {'id': 'comicimage'})[0]['src']
            print('Downloading:', page_number, url + img_link)
            r = requests.get(url + img_link, stream=True)  # get file stream

            async with aiofiles.open(path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=2048):
                    if chunk:
                        await f.write(chunk)
                    else:
                        print(chunk)

        await asyncio.sleep(0)

    num = 0
    added_frames = 0
    added_gifs = 0

    for j, (key, value) in enumerate(data.items(), 2):
        image = '{}.jpg'.format(j)
        result = await split_page(image, num, pages_dir, frames_dir, gif_dir)
        num = result[0]

        if result[1] > 0:
            data[key] = result[0], result[1]

        added_frames += result[1]
        added_gifs += result[2]
        await asyncio.sleep(0)

    print(data)
    l = list(data.items())
    print(*sorted(l, key=lambda x: x[1][1]), sep='\n')
    with open(os.path.abspath(databse), 'wb') as f:
        pickle.dump([arcs, data], f)

    return added_frames, added_gifs


def get_timing(num):
    if os.path.exists(os.path.abspath(user_votes_file)):
        with open(os.path.abspath(user_votes_file), 'rb') as f:
            votes = pickle.load(f)
    else:
        return 250

    timings = votes[num]
    return round(statistics.mean(timings.values() if timings else [250]))


async def split_page(image_name, global_numeration=0, pages_dir='pages/', frames_dir='frames/', gif_dir='gif/',
                     load_timings=False):

    if not os.path.exists(os.path.abspath(frames_dir)):
        os.mkdir(os.path.abspath(frames_dir))

    if not os.path.exists(os.path.abspath(gif_dir)):
        os.mkdir(os.path.abspath(gif_dir))

    try:
        loop = asyncio.get_running_loop()
    except AttributeError:
        loop = asyncio.get_event_loop()

    added_frames = 0
    added_gifs = 0

    im = Image.open(os.path.abspath(pages_dir + image_name))
    count = im.size[1] // 338

    frames = []
    timings = []

    print('Splitting page:', image_name, 'Frames done:', global_numeration, "to: ", frames_dir)
    gif_path = os.path.abspath(gif_dir + image_name.split(".")[0] + '.gif')

    for i in range(count):
        frame_path = os.path.abspath(frames_dir + str(global_numeration) + '.jpg')
        if (not os.path.exists(gif_path)) or (not os.path.exists(frame_path)):

            region = await loop.run_in_executor(None, partial(process_page, im, i))

            if not os.path.exists(frame_path):
                await loop.run_in_executor(None, partial(save_frame, region, frame_path))
                added_frames += 1

            if not os.path.exists(gif_path):
                region = await loop.run_in_executor(None, partial(process_gif, region))
                frames.append(region)  # for gifs
                if load_timings:
                    timings.append(get_timing(global_numeration))

        global_numeration += 1
        await asyncio.sleep(0)

    if not os.path.exists(gif_path):
        if load_timings:
            await loop.run_in_executor(None, partial(save_gif, frames, gif_path, timings))
        else:
            await loop.run_in_executor(None, partial(save_gif, frames, gif_path))

        added_gifs += 1

    return global_numeration, added_frames, added_gifs


if __name__ == "__main__":
    async def main():
        downloaded = await pull_comic()
        print("Downloaded and split {} new frames and {} new gif animations!".format(
            *downloaded))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
