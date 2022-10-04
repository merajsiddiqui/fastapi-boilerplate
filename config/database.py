from decouple import config
from urllib.parse import urlencode


def build_db_url():
    driver = urlencode(config('DB_DRIVER'))
    user = urlencode(config('DB_USER'))
    password = urlencode(config('DB_PASSWORD'))
    host = urlencode(config('DB_HOST'))
    database = urlencode(config('DB_NAME'))
    port = urlencode(config('DB_PORT'))
    return '{}://{}:{}@{}/{}:{}'.format(driver, user, password, host, database, port)
