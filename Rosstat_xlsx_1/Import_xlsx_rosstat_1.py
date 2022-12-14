import requests
from bs4 import BeautifulSoup
import os.path


def import_xlsx_fun(url: str) -> (str | bool):
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        divs = soup.select("div.document-list__item-link")
        xlsx = divs[0].select_one("a").attrs["href"]
        xlsx = "https://rosstat.gov.ru" + xlsx

        with open(os.path.basename(xlsx).format(xlsx), "wb") as file:
            file.write(requests.get(xlsx).content)

        return os.path.basename(xlsx).format(xlsx)
    except OSError:
        print("Не работает сохранение файла (Поменялся сайт)")
        print("Ошибка в файле 'Import_xlsx_rosstat_1.py'")
        return False


def import_xlsx_rosstat() -> (str | bool):
    file_name = import_xlsx_fun("https://rosstat.gov.ru/compendium/document/13282")
    return file_name
