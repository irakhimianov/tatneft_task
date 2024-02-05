import asyncio
import logging
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import aiohttp

logger = logging.getLogger(__name__)


class InvalidUrlError(Exception):
    ...


def get_save_path(path: Optional[Path | str] = None) -> Path:
    """
    Получение и проверка пути для сохранения файлов. Если такой путь не существует на
    файловой системе - то такой путь создается
    :param path: Желаемый путь для сохранения, по умолчанию директория со скриптом и папка `./downloads`
    :type path: Path, optional
    :return: Путь сохранения
    :rtype: Path
    """
    if path is None:
        path = Path.cwd() / 'downloads'

    if isinstance(path, str):
        path = Path(path)

    path.mkdir(parents=True, exist_ok=True)
    return path


def format_url(url: str) -> str:
    """
    Приведение URL-адреса в порядок
    :param url: Исходный URl-адрес
    :type url: str
    :return: Отформатированный URL-адрес
    :rtype: str
    :raises: InvalidUrlError
    """
    parsed = urlparse(url)
    if not parsed.scheme:
        return f'http://{url}'

    if parsed.scheme in ('http', 'https'):
        return url

    raise InvalidUrlError(f'Недопустимый URL-адрес: {url}')


async def save_html_page(session: aiohttp.ClientSession, url: str, save_path: Optional[Path | str] = None) -> None:
    """
    Сохраняет html-страницу интернет-ресурса в файловой системе
    :param session:
    :type session: aiohttp.ClientSession
    :param url: URL-адрес ресурса
    :type url: str
    :param save_path: Желаемый путь для сохранения
    :type save_path: Path, str,  optional
    """
    try:
        url = format_url(url)
        path = get_save_path(path=save_path)
        async with session.get(url) as response:
            if response.status != 200:
                logger.info(f'Запрос к {url} не закончился успехом: {response.status}')

            file_path = path / f'{urlparse(url).netloc}.html'
            page_content = await response.text()
            with open(file_path, 'w') as f:
                f.write(page_content)
    except InvalidUrlError as e:
        logger.error(e)
    except aiohttp.ClientError as e:
        logger.error(f'Ошибка во время выполнения запроса к {url}: {e}')


async def save_html_pages(urls: list[str], save_path: Optional[Path | str] = None) -> None:
    """
    Сохраняет html-страницы списка интернет-ресурсов в файловой системе
    :param urls: Список URL-адресов интернет-ресурсов
    :type urls: list[str]
    :param save_path: Желаемый путь для сохранения
    :type save_path: Path, str,  optional
    """
    async with aiohttp.ClientSession() as session:
        tasks = [save_html_page(session=session, url=url, save_path=save_path) for url in urls]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    urls = []
    loop = asyncio.get_event_loop()
    loop.run_until_complete(save_html_pages(urls=urls))
