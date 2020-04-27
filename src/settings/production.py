from .base import *

SECRET_KEY = env("SECRET_KEY")

DEBUG = False

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
