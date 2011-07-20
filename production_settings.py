from settings import *
import os

LIB_PATH = os.path.join(ROOT_PATH, 'lib')

for directory in os.listdir(LIB_PATH):
    sys.path.insert(0, os.path.join(LIB_PATH, directory))


DEBUG = False
SITE_ID = 2
