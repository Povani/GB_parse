import time
import json
from pathlib import Path
import requests
from urllib.parse import urlparse


class Parse5ka:
# headers - необходмо, что бы сайт, видел нас как браузер

    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0"}

# в метод ниже передаем адрес документа для парсинга и путь сохранения для данных

    def __init__(self, start_url: str, save_path: Path):
        self.start_url = start_url
        self.save_path = save_path


# в методе _get_response(self, url) получаем на входе ссылку на документ и возвращаем ссылки на документы
# со статусом ответа равным 200
    def _get_response(self, url):
        url = url.replace(urlparse(url).netloc, urlparse(self.start_url).netloc)
        while True:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response
            time.sleep(0.1)

#    def run(self):
#       for product in self._parse(self.start_url):
#            product_path = self.save_path.joinpath(f"{product['id']}.json")
#            self._save(product, product_path)


    def _parse(self, url: str):
        while url:
            response = self._get_response(url)
            data: dict = response.json()
            url = data["next"]
            for product in data["results"]:
                yield product

    def _save(self, data: dict, file_path: Path):
        file_path.write_text(json.dumps(data, ensure_ascii=False))


class CategoriesParser(Parse5ka):
    def __init__(self, categories_url, *args, **kwargs):
        self.categories_url = categories_url
        super().__init__(*args, **kwargs)

    def _get_categories(self):
        response = self._get_response(self.categories_url)
        data = response.json()
        return data

    def run(self):
        for category in self._get_categories():
            category["products"] = []
            params = f"?categories={category['parent_group_code']}"
            url = f"{self.start_url}{params}"
            category["products"].extend(list(self._parse(url)))
            file_name = f"{category['parent_group_code']}.json"
            cat_path = self.save_path.joinpath(file_name)
            self._save(category, cat_path)


# Функция ниже производит создание дериктории, в случае отсутствия и создает путь для сохранения в данную дерикторию
def get_save_path(dir_name):
    save_path = Path(__file__).parent.joinpath(dir_name)
    if not save_path.exists():
        save_path.mkdir()
    return save_path


if __name__ == "__main__":
    url = "https://5ka.ru/api/v2/special_offers/"
    cat_url = "https://5ka.ru/api/v2/categories/"
#    save_path_products = get_save_path("products")
    save_path_categories = get_save_path("categories")
#    parser_products = Parse5ka(url, save_path_products)
    category_parser = CategoriesParser(cat_url, url, save_path_categories)
    category_parser.run()
