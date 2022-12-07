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
        return False


def input_output_txt(text):
    with open("Output.txt", "w") as f:
        f.write(text)
        f.close()


def main():
    input_output_txt(import_xlsx_fun("https://rosstat.gov.ru/compendium/document/13282"))


main()