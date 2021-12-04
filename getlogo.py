#!/usr/bin/env python3
import re
from urllib.request import urlopen
import sys
import re

RE_IMG_URL = re.compile(
    r'<img class="tgme_page_photo_image" src="(.+)"'
)

def main(**kwargs):
    username = sys.argv[1]
    logoname = sys.argv[2]
    assert logoname.endswith('.jpg')
    url = 'https://t.me/%s' % username
    html = urlopen(url).read().decode('utf-8')
    img_url = RE_IMG_URL.search(html).group(1)
    print('Downloading %s' % img_url)
    img_data = urlopen(img_url).read()
    logo_path = 'static/logo/%s' % logoname
    with open(logo_path, 'wb') as out:
        out.write(img_data)
    print('Saved %d bytes to %s' % (len(img_data), logo_path))

if __name__ == '__main__':
    main()
