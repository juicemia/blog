#!/usr/bin/env python3

from markdown import markdown
from yaml import load, FullLoader
from sys import exit
from os import mkdir
from shutil import copytree
from jinja2 import Environment, FileSystemLoader, select_autoescape

import codecs

try:
    mkdir('www')
except FileExistsError:
    print('www already exists, skipping build...')
    exit(1)

# FileExistsError can't be thrown here because 'www' is guaranteed to be empty above.
mkdir('www/blog')

copytree('static/css', 'www/css')
copytree('static/webfonts', 'www/webfonts')
copytree('static/js', 'www/js')
copytree('static/img', 'www/img')

with open('gen.yml') as f:
    config = load(f.read(), Loader=FullLoader)

title = config['title']
siteConfig = config['site']

env = Environment(loader=FileSystemLoader('templates'), autoescape=select_autoescape([]))
basetpl = env.get_template('base.tpl.html')

for key in siteConfig:
    pageConfig = siteConfig[key]

    with codecs.open('content/{}'.format(pageConfig['source']), encoding='UTF-8') as input_file, \
        codecs.open('www/{}'.format(key), 'w+', encoding='UTF-8') as output_file:

        buf = input_file.read()
        content = markdown(buf)
        output_file.write(basetpl.render(title=title, content=content))
