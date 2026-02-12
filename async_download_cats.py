"""Асинхронная версия скачивания котиков."""
import asyncio
from datetime import datetime
from pathlib import Path

import aiofiles
import aiofiles.os
import aiohttp

URL = 'https://api.thecatapi.com/v1/images/search'
BASE_DIR = Path(__file__).parent
CATS_DIR = BASE_DIR / 'cats'


async def get_new_image_url():
    """Асинхронно получает новое изображения."""
    # Создаёт асинхронную сессию для выполнения HTTP-запроса.
    async with aiohttp.ClientSession() as session:
        # Выполняет асинхронный GET-запрос на URL.
        response = await session.get(URL)
        # Асинхронно получает тело ответа в формате JSON.
        data = await response.json()

        return data[0]['url']


async def download_file(url):
    """Асинхронно загружает файлы по URL."""
    filename = url.split('/')[-1]
    # Создать асинхронную сессию для выполнения HTTP-запроса.
    async with aiohttp.ClientSession() as session:
        # Выполнить асинхронный GET-запрос по заданному URL.
        result = await session.get(url)
        async with aiofiles.open(CATS_DIR / filename, 'wb') as file:
            # Прочитать содержимое ответа и записать его в файл.
            await file.write(await result.read())


async def download_new_cat_image():
    """Асинхронно получает URL картинки и скачивает её."""
    url = await get_new_image_url()
    await download_file(url)


async def create_dir(dir_name):
    """Асинхронно создаёт директорию."""
    await aiofiles.os.makedirs(
        dir_name,
        exist_ok=True
    )


async def list_dir(dir_name):
    """Асинхронно получает список файлов директории."""
    files_and_dirs = await aiofiles.os.listdir(dir_name)
    print(*files_and_dirs, sep='\n')


async def main():
    """Главная асинхронная функция."""
    await create_dir(CATS_DIR)
    tasks = [
        # Асинхронно выполнять функцию 100 раз.
        asyncio.ensure_future(download_new_cat_image()) for _ in range(100)
    ]
    # Подождать, пока выполнятся все задачи.
    await asyncio.wait(tasks)


if __name__ == '__main__':
    start_time = datetime.now()
    # Получить текущий событийный цикл.
    loop = asyncio.get_event_loop()
    # Запустить основную корутину и подождать, пока она завершиться.
    loop.run_until_complete(main())
    full_time = datetime.now() - start_time
    print(f'Время выполнения программы: {full_time}.')
    asyncio.run(list_dir(CATS_DIR))
