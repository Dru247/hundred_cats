"""Скачивает котиков в файлы."""
import os
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
URL = 'https://api.thecatapi.com/v1/images/search'
CATS_DIR = CATS_DIR = BASE_DIR / 'cats'
PROXY_HOST = os.getenv('PROXY_HOST')
PROXY_PORT = os.getenv('PROXY_PORT')
PROXY_LOGIN = os.getenv('PROXY_LOGIN')
PROXY_PASSWORD = os.getenv('PROXY_PASSWORD')
PROXY_URL = f'socks5://{PROXY_LOGIN}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}'
REQUEST_TIMEOUT = 10

proxies = {
    'http': PROXY_URL,
    'https': PROXY_URL
}


def get_new_image_url() -> str:
    """Возвращет URL фото нового котика."""
    response = requests.get(
        url=URL,
        proxies=proxies,
        timeout=REQUEST_TIMEOUT
    ).json()
    return response[0].get('url')


def download_file(url: str) -> None:
    """Скачивает и записывает фото котика."""
    filename = url.split('/')[-1]
    response = requests.get(url)
    response.raise_for_status()  # Проверка, что запрос выполнен успешно
    with open(CATS_DIR / filename, 'wb') as file:
        file.write(response.content)


def download_new_cat_image() -> None:
    """Скачавает фото котика через URL."""
    url = get_new_image_url()
    download_file(url)


def create_dir(dir_name) -> None:
    """Создаёт директорию под котиков."""
    os.makedirs(dir_name, exist_ok=True)


def list_dir(dir_name) -> None:
    """Печатает содержание дирректории."""
    print(
        *os.listdir(dir_name),
        sep='\n'
    )


def main() -> None:
    """Создаёт директориюи скачивает фото котиков."""
    create_dir(CATS_DIR)
    for _ in range(100):
        download_new_cat_image()


if __name__ == '__main__':
    start_time = datetime.now()
    main()
    final_time = datetime.now() - start_time
    print(f'Время выполнения программы: {final_time}.')
    list_dir(CATS_DIR)
