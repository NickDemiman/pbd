from dotenv import load_dotenv
import os
from modules.ctg_api import *
from modules.tag_api import *
from modules.app_api import AppCrawler
from modules.db_manager import DBManager
import argparse


def main():
    if (os.path.exists('./.env')):
        load_dotenv('./.env')
    else:
        raise BaseException('Файл настроек не найден (.env)')

    WEB_API_KEY = os.environ.get("WEB_API_KEY", None)
    manager = DBManager()
    
    parser = argparse.ArgumentParser(
        "fill_db Script",
    )
    
    parser.add_argument(
        '-c', '--create',
        action="store_true",
        help="Выполнить все create скрипты на типы и таблицы"
    )
    
    parser.add_argument(
        '-append', '--append',
        action="store_true",
        help="Дозагрузить приложения в БД"
    )    
    
    parser.add_argument(
        '-count',
        dest='count',
        default=10,
        type=int,
        help="Кол-во приложений для добавления"
    )    
    
    parser.add_argument(
        '-tags', '--tags',
        action="store_true",
        help="Загрузить записи с тегами в БД"
    )
    
    parser.add_argument(
        '-categories', '--categories',
        action="store_true",
        help="Загрузить записи с категориями в БД"
    )
    
    args = parser.parse_args()

    
    if (args.create):
        manager.create()
    
    tags = get_tags(WEB_API_KEY)
    
    if args.tags:
        manager.add_tags(tags)
        manager.commit()
        print(f"Total Tags added - {len(tags)}")
    
    
    categories = get_categories(WEB_API_KEY)
    if args.categories:
        manager.add_categories(categories)
        manager.commit()
        print(f"Total Categories added - {len(categories)}")
    
    appCrawler = AppCrawler(manager, tags)
    
    if args.append:
        last = manager.get_last_app_id()
        apps, labels = appCrawler.get_apps(args.count, id_start=last)
    else:
        apps, labels = appCrawler.get_apps(args.count)
    
    if (len(apps) != 0): 
        manager.add_apps(apps, labels)
        manager.commit()


if __name__ == '__main__':
    main()
