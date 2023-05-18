#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

BIND = "127.0.0.1"

AUTHOR = 'Scott Pease'
SITENAME = "Scott's Stuff"
SITEURL = ''

PATH = 'content'
OUTPUT_PATH = '..'

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),)

# Social widget
SOCIAL = (('github', 'https://github.com/swpease'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# https://github.com/pelican-plugins/render-math
# MATH_JAX = {'color':'blue'}
