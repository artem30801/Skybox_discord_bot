import os
import asyncio
import skybox_fetcher

pages_dir = 'translated_pages/'
frames_dir = 'translated_frames/'
gif_dir = 'translated_gif/'

if not os.path.exists(os.path.abspath(frames_dir)):
    os.mkdir(os.path.abspath(frames_dir))

if not os.path.exists(os.path.abspath(gif_dir)):
    os.mkdir(os.path.abspath(gif_dir))


async def split_all():
    for image in os.listdir(os.path.abspath(pages_dir)):
        result = await skybox_fetcher.split_page(image, 0,
                                                 pages_dir, frames_dir+image.split(".")[0]+'/', gif_dir, True)
        print(result)


loop = asyncio.get_event_loop()
loop.run_until_complete(split_all())
