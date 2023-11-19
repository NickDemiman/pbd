from requests import get
from psycopg2.extras import DictCursor

def get_tags(key: str):
    tags_list_raw = get("https://api.steampowered.com/IStoreService/GetMostPopularTags/v1/", {
        "key": key
    }).json()\
        .get('response')\
        .get('tags')

    tags = [(
        tag_raw['tagid'], 
        tag_raw['name']
        ) for tag_raw in tags_list_raw]

    return tags
