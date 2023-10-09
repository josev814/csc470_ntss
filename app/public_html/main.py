#!/usr/bin/env python3
"""
The NTSS app
"""
#import cgitb
from os import path
import configparser
from jinja2 import Environment, FileSystemLoader, select_autoescape
#cgitb.enable()

print('Content-type: text/html')
print()



this_file_abs = path.realpath(__file__).split('/')
this_file_abs.pop()
this_file_abs.pop()
BASEDIR = '/'.join(this_file_abs)
DATABASE = None
CONFIGFILE = path.join('/bin', 'settings', 'config.txt')
cp = configparser.ConfigParser()
cp.read(CONFIGFILE)

if 'database' in cp.sections() and cp.has_option('database', 'driver'):
    driver_type = cp.get('database', 'driver')
    if driver_type in cp.sections():
        if driver_type == 'mysql':
            pass


env = Environment(
    loader=FileSystemLoader('views'),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('index.html')

print(
    template.render(
    )
)
