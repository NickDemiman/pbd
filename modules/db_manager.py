from psycopg2.extras import DictCursor
import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.errors import Error


BASE_DIR_TABLES = os.path.abspath('./modules/db_scripts')
BASE_DIR_TYPES =  os.path.abspath('./modules/db_scripts/types')


class DBManager:
    def __init__(self, autocommit = False, env_file_path = '.env'):
        if (os.path.exists(env_file_path)):
            load_dotenv(env_file_path)
        else:
            raise BaseException(f'Файл настроек не найден {env_file_path}')

        host = os.environ.get('POSTGRESQL_HOST', None)
        user = os.environ.get('POSTGRESQL_USER', None)
        password = os.environ.get('POSTGRESQL_PASSWORD', None)
        database = os.environ.get('POSTGRESQL_DATABASE', None)

        if not host:
            raise BaseException('Не найдено значение "POSTGRESQL_HOST" в переменных среды')
        
        if not user:
            raise BaseException('Не найдено значение "POSTGRESQL_USER" в переменных среды')

        if not password:
            raise BaseException('Не найдено значение "POSTGRESQL_PASSWORD" в переменных среды')

        if not database:
            raise BaseException('Не найдено значение "POSTGRESQL_DATABASE" в переменных среды')

        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()
        self.connection.autocommit = autocommit

    def create(self):
        self.connection.autocommit = True
        self.create_type_achievement()
        self.create_type_achievements()
        self.create_type_package()
        self.create_type_package_group()
        self.create_type_platforms()
        self.create_type_price_overview()
        self.create_type_release_date()
        self.create_type_requirements()
        self.create_type_screenshot()
        self.create_type_support_info()
        self.create_app()
        self.create_category()
        self.create_tag()
        self.create_app_category()
        self.create_app_tag()
        self.connection.autocommit = False
    
    def commit(self):
        self.connection.commit()

    # region Create Scripts
    def create_app(self):
        with open(os.path.join(BASE_DIR_TABLES, 'app_create.sql')) as file:
            query = '\n'.join(file.readlines())
            self.cursor.execute(query)
            
    def create_category(self):
        with open(os.path.join(BASE_DIR_TABLES, "category_create.sql")) as file:
            query = '\n'.join(file.readlines())
            self.cursor.execute(query)
            
    def get_db_size(self):
        with open(os.path.join(BASE_DIR_TABLES, "get_db_size_mb.sql")) as file:
            query = '\n'.join(file.readlines())
            self.cursor.execute(query)
            
    def create_tag(self):
        with open(os.path.join(BASE_DIR_TABLES, "tag_create.sql")) as file:
            query = '\n'.join(file.readlines())
            self.cursor.execute(query)
            
    def create_app_category(self):
        with open(os.path.join(BASE_DIR_TABLES, "app_category.sql")) as file:
            query = '\n'.join(file.readlines())
            self.cursor.execute(query)
            
    def create_app_tag(self):
        with open(os.path.join(BASE_DIR_TABLES, "app_tag.sql")) as file:
            query = '\n'.join(file.readlines())
            self.cursor.execute(query)

    def create_type_achievement(self):
        with open(os.path.join(BASE_DIR_TYPES, "achievement.sql")) as file:
            query = '\n'.join(file.readlines())
            try:
                self.cursor.execute(query)
            except Error as e:
                print(e)
            
    def create_type_achievements(self):
        with open(os.path.join(BASE_DIR_TYPES, "achievements.sql")) as file:
            query = '\n'.join(file.readlines())
            try:
                self.cursor.execute(query)
            except Error as e:
                print(e)

    def create_type_package(self):
        with open(os.path.join(BASE_DIR_TYPES, "package.sql")) as file:
            query = '\n'.join(file.readlines())
            try:
                self.cursor.execute(query)
            except Error as e:
                print(e)

    def create_type_package_group(self):
        with open(os.path.join(BASE_DIR_TYPES, "package_group.sql")) as file:
            query = '\n'.join(file.readlines())
            try:
                self.cursor.execute(query)
            except Error as e:
                print(e)

    def create_type_platforms(self):
        with open(os.path.join(BASE_DIR_TYPES, "platforms.sql")) as file:
            query = '\n'.join(file.readlines())
            try:
                self.cursor.execute(query)
            except Error as e:
                print(e)

    def create_type_price_overview(self):
        with open(os.path.join(BASE_DIR_TYPES, "price_overview.sql")) as file:
            query = '\n'.join(file.readlines())
            try:
                self.cursor.execute(query)
            except Error as e:
                print(e)

    def create_type_release_date(self):
        with open(os.path.join(BASE_DIR_TYPES, "release_date.sql")) as file:
            query = '\n'.join(file.readlines())
            try:
                self.cursor.execute(query)
            except Error as e:
                print(e)

    def create_type_requirements(self):
        with open(os.path.join(BASE_DIR_TYPES, "requirements.sql")) as file:
            query = '\n'.join(file.readlines())
            try:
                self.cursor.execute(query)
            except Error as e:
                print(e)

    def create_type_screenshot(self):
        with open(os.path.join(BASE_DIR_TYPES, "screenshot.sql")) as file:
            query = '\n'.join(file.readlines())
            try:
                self.cursor.execute(query)
            except Error as e:
                print(e)

    def create_type_support_info(self):
        with open(os.path.join(BASE_DIR_TYPES, "support_info.sql")) as file:
            query = '\n'.join(file.readlines())
            try:
                self.cursor.execute(query)
            except Error as e:
                print(e)
    # endregion
    
    # region Truncate Scripts
    def truncate_app(self):
       self.cursor.execute('truncate table "App" cascade;')

    def truncate_app_category(self):
       self.cursor.execute('truncate table "App_Category" cascade;')

    def truncate_app_tag(self):
       self.cursor.execute('truncate table "App_Tag" cascade;')

    def truncate_category(self):
       self.cursor.execute('truncate table "Category" cascade;')

    def truncate_tag(self):
       self.cursor.execute('truncate table "Tag" cascade;')
    # endregion
    
    # region Tags
    def add_tags(self, tags: list[tuple]):
        args = ','.join(self.cursor.mogrify("(%s, %s)", tag).decode('utf-8')
                    for tag in tags)
        try:
            self.cursor.execute('INSERT INTO public."Tag"("tagid", "name") VALUES ' + (args))
        except Error as e:
            print(e)

    def add_app_tag(self, appid: str, app_tags: list, tags: list):
        def find_tag_id(tag_name):
            for tag in tags:
                if (tag_name == tag[1]):
                    return tag[0]
            return

        records = []
        for app_tag in app_tags:
            tagid = find_tag_id(app_tag)
            if tagid != None:
                records.append((appid, tagid))
        if len(records) != 0:
            args = ','.join(self.cursor.mogrify("(%s, %s)", rec).decode('utf-8')
                            for rec in records)
            try:
                self.cursor.execute('INSERT INTO public."App_Tag"("appid", "tagid") VALUES ' + (args))
            except Error as e:
                print(e)
    
    def get_tags(self, explain=False):
        try:
            query = 'SELECT * FROM public."Tag"'
            if explain:
                self.cursor.execute('explain ' + query)
            else:
                self.cursor.execute(query)
            self.commit()
            tags = self.cursor.fetchall()
        except Error as e:
            print(e)
        return tags
        
    # endregion
    
    # region Category
    def add_categories(self, categories: list[tuple]):
        args = ','.join(self.cursor.mogrify("(%s, %s, %s, %s, %s)", category).decode('utf-8')
                        for category in categories)
        try:
            self.cursor.execute('INSERT INTO public."Category"("categoryid", "type", "internal_name", "display_name", "image_url") VALUES ' + (args))
        except Error as e:
            print(e)
        
    def add_app_ctg(self, appid: str, ctgs: list):
        records = [(appid, ctg) for ctg in ctgs]

        args = ','.join(self.cursor.mogrify("(%s, %s)", rec).decode('utf-8')
                        for rec in records)
        
        try:
            self.cursor.execute('insert into public."App_Category"("appid", "categoryid") values ' + (args))
        except Error as e:
            print(e)
    
    def get_categories(self, explain=False):
        try:
            query = 'SELECT * FROM public."Category"'
            if explain:
                self.cursor.execute('explain ' + query)
            else:
                self.cursor.execute(query)
            self.commit()
            categories = self.cursor.fetchall()
        except Error as e:
            print(e)
        return categories
    # endregion
    
    # region Apps
    def add_apps(self, apps: list, labels: list):
        self.cursor.execute(f'select steam_appid from public."App"')
        app_ids = self.cursor.fetchall()
        if (app_ids):
            app_ids = [_id[0] for _id in app_ids]
            apps = [app for app in apps if app[0] not in app_ids]
            
        formatter = "(" + ','.join([label[1] for label in labels])+")"
        args = ','.join([self.cursor.mogrify(formatter, app).decode('utf-8') for app in apps])
        columns = ','.join([label[0] for label in labels])
        if (apps):
            try:
                self.cursor.execute(f'INSERT INTO public."App"({columns}) VALUES ' + (args))
                print(f"Total Apps added - {len(apps)}")
            except Error as e:
                print(e)
        else:
            print("При загрузке были повторы steam_appid, Total: 0")
        
    
    def get_last_app_id(self):
        self.cursor.execute('select steam_appid from public."App"')
        data = self.cursor.fetchall()
        if data:
            return data[-1][0]
        else:
            return 0
    
    def get_apps(self, explain=False):
        try:
            query = 'SELECT * FROM public."App"'
            if (explain):
                self.cursor.execute('explain ' + query)
            else:
                self.cursor.execute(query)
            self.commit()
            apps = self.cursor.fetchall()
        except Error as e:
            print(e)
        return apps
    # endregion