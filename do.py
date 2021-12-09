#!/usr/bin/env python3
from pprint import pprint
import json
import re
from urllib.request import urlopen
import sys
import re
import shutil
from html import unescape

RE_TME_IMG_URL = re.compile(
    r'<img class="tgme_page_photo_image" src="(.+)"'
)
RE_TME_TITLE = re.compile(
    r'tgme_page_title[^>]+>\s*<span[^>]+>([^<]+)'
)
USER_PLACEHOLDER_IMAGE = 'static/logo/user.jpg'
NODES_JSON_FILE = 'data/nodes.json'
NODES_COMPILED_FILE = 'static/data/nodes.js'
#ID_ROOT_NODE = 'scope-ru-osint-infosec'


def build_tme_url(username):
    return 'https://t.me/%s' % username


def get_tme_page(username):
    url = build_tme_url(username)
    html = urlopen(url).read().decode('utf-8')
    return html


def action_getlogo(username, gid, html=None):
    if html is None:
        html = get_tme_page(username)
    match = RE_TME_IMG_URL.search(html)
    logo_path = 'static/logo/%s.jpg' % gid
    if not match:
        print('No image found, using placeholder')
        shutil.copyfile(USER_PLACEHOLDER_IMAGE, logo_path)
    else:
        img_url = match.group(1)
        print('Downloading %s' % img_url)
        img_data = urlopen(img_url).read()
        with open(logo_path, 'wb') as out:
            out.write(img_data)
        print('Saved %d bytes to %s' % (len(img_data), logo_path))
    return logo_path


def action_add(node_type, username, gid):
    assert node_type in [
        'user', 'channel', 'group',
        'website', 'twitter', 'youtube'
    ]
    if node_type in ['user', 'channel', 'group']:
        if username == 'BLANK':
            name = '???'
            if node_type == 'user':
                logo_path = 'static/logo/user.jpg'
            else:
                logo_path = ''
            url = None
        else:
            html = get_tme_page(username)
            name = unescape(RE_TME_TITLE.search(html).group(1))
            logo_path = action_getlogo(username, gid, html=html)
            url = build_tme_url(username)
    else:
        name = ''
        logo_path = ''
        url = None
    item = {
        'id': gid,
        'name': name,
        'type': node_type,
        'links': [],
        'imageUrl': logo_path,
        'url': url,
    }
    with open(NODES_JSON_FILE) as inp:
        data = json.load(inp)
    print('Loaded %d items from JSON file' % len(data))
    #if node_type == 'user':
    #    for node in data:
    #        if node['id'] == ID_ROOT_NODE:
    #            if not gid in node['links']:
    #                node['links'].append(gid)
    data.append(item)
    print('Saved %d items to JSON file' % len(data))
    with open(NODES_JSON_FILE, 'w') as out:
        out.write(json.dumps(data, indent=4, ensure_ascii=False))
    action_compile()


def action_compile():
    with open(NODES_JSON_FILE) as inp:
        data = json.load(inp)
    with open(NODES_COMPILED_FILE, 'w') as out:
        json_data = json.dumps(data, indent=4, ensure_ascii=False)
        out.write('dataNodes = %s;' % json_data)
    print('Saved %d items to JS compiled file %s' % (
        len(data), NODES_COMPILED_FILE
    ))


def main(**kwargs):
    action = sys.argv[1]
    if action == 'getlogo':
        username = sys.argv[2]
        gid = sys.argv[3]
        action_getlogo(username, gid)
    elif action == 'add':
        node_type = sys.argv[2]
        username = sys.argv[3]
        gid = sys.argv[4]
        action_add(node_type, username, gid)
    elif action == 'compile':
        action_compile()
    else:
        sys.stderr.write('Unknown action: %s' % action)
        sys.exit(1)


if __name__ == '__main__':
   main() 
