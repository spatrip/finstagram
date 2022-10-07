
"""Insta485 development configuration."""
import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SK = b'$=\xed\x1dh\x13(\xdb\xd8w\x1aa\xa6\x16G\xc2\xcdH\xbf\xeb \x1f8\xf4'
SECRET_KEY = SK
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
INSTA485_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = INSTA485_ROOT/'var'/'uploads'
STATIC_IMAGES_FOLDER = INSTA485_ROOT/'insta485'/'static'/'images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/insta485.sqlite3
DATABASE_FILENAME = INSTA485_ROOT/'var'/'insta485.sqlite3'
