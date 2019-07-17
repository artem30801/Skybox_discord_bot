import os
import re
import time
import requests

frames_dir = 'translated_frames/'
post_num_delta = 82

cookies = {
    'unpin': 'false',
    'username': 'Striga',
    'hash': 'c596b13d0a7d2303132c306fc3bdc432',
    'PHPSESSID': 'c332d3179c50352fa8a9acc916e76f17'
}

headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                     "application/signed-exchange;v=b3",
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
           "Cache-Control": "max-age=0",
           "Upgrade-Insecure-Requests": "1",
           "Origin": "https://acomics.ru",
           "Referer": "https://acomics.ru/manage/addIssue?id=7185",
           "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         'Chrome/73.0.3683.103 Safari/537.36'}


def post_ak(post_num, delta, act_num, frames_path=frames_dir, is_im=False):
    if not is_im:
        name = "Акт {} - {}".format(act_num, str(post_num - delta).zfill(2))
    else:
        name = "Акт {} - Чат-вставка {}".format(act_num, str(is_im).zfill(2))
    data = {
        "altText": "",
        "description":  '<hr />'
                        '<p>'
                        '<span style="font-size:13px;">Будем рады видеть вас в нашей </span><a href="https://vk.com/skyboxcomic"><span style="font-size:15px;">группе ВКонтакте</span></a>, <span style="font-size:13px;">где мы публикуем различные дополнительные материалы по комиксу!</span>'
                        '</p>',
        "name": name,
        "number": "",
        "numberOrder": "on",
        "originalUrl": "http://www.skyboxcomic.com/comics/{}".format(post_num),
        "publish": "instant",
        "serialId": "7185",
        "submit": "add"
    }
    path = frames_path + str(post_num) + '/'
    with requests.Session() as s:
        for frame in sorted(os.listdir(os.path.abspath(path)),
                            key=lambda var: [int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)]):

            files = {
                "image": (frame, open(os.path.abspath(path+frame), 'rb'), 'image/jpeg')
            }

            r = s.post('https://acomics.ru/action/manageAddIssue',
                       data=data, files=files, headers=headers, cookies=cookies)
            print(r.text)
            time.sleep(2)


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1", "y")


if __name__ == "__main__":
    p_num = int(input("Post/folder num: "))
    im = str2bool(input("Is that IM break? "))
    if im:
        im = int(input("Im num: "))
    a_num = int(input("Arc num: "))

    post_ak(p_num, post_num_delta, a_num, frames_dir, im)
