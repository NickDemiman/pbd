from requests import get
from psycopg2.extras import DictCursor


def get_categories(key: str):
    categories_raw = get("https://api.steampowered.com/IStoreBrowseService/GetStoreCategories/v1/", {
        "key": key,
        "language": "english"
    }).json()\
        .get('response')\
        .get('categories')

    categories = [(
        category_raw['categoryid'],
        category_raw['type'],
        category_raw['internal_name'],
        category_raw['display_name'],
        category_raw['image_url']
        ) for category_raw in categories_raw]

    return categories