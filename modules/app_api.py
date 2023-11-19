from requests import get
import time
from aiohttp import ClientSession
import asyncio
from math import ceil
from tqdm import tqdm 
from modules.db_manager import DBManager


class AppCrawler:
    def __init__(self, manager: DBManager, tags: list):
        self.labels = (
            ("steam_appid", "%s"), 
            ("name", "%s"), 
            ("type", "%s::varchar"), 
            ("required_age", "%s"), 
            ("is_free", "%s"), 
            ("detailed_description", "%s"), 
            ("about_the_game", "%s"), 
            ("short_description", "%s"), 
            ("supported_languages", "%s"), 
            ("header_image", "%s"), 
            ("website", "%s"), 
            ("pc_requirements", "%s::requirements"), 
            ("mac_requirements", "%s::requirements"), 
            ("linux_requirements", "%s::requirements"), 
            ("legal_notice", "%s"), 
            ("developers", "%s"), 
            ("publishers", "%s"), 
            ("price_overview", "%s::price_overview"), 
            # packages, pckg_groups
            ("platforms", "%s::platforms"), 
            ("screenshots", "%s::screenshot[]"), 
            # ("achievements", "%s::achievements"), 
            # release_date, support_info
            ("background", "%s"), 
            ("background_raw", "%s"), 
        )
        self.__tags = tags
        self.__manager = manager

    def __get_app_field_values(self, app: dict):
        steam_appid = app.get("steam_appid")
        name = app.get("name")
        _type = app.get("type")
        required_age = app.get("required_age")
        is_free = app.get("is_free")
        detailed_description = app.get("detailed_description")
        about_the_game = app.get("about_the_game")
        short_description = app.get("short_description")
        supported_languages = app.get("supported_languages")
        header_image = app.get("header_image")
        website = app.get("website")
        pc_requirements = app.get("pc_requirements")
        mac_requirements = app.get("mac_requirements")
        linux_requirements = app.get("linux_requirements")
        legal_notice = app.get("legal_notice")
        developers = app.get("developers")
        publishers = app.get("publishers")
        price_overview = app.get("price_overview")
        categories = app.get("categories")
        genres = app.get("genres")
        platforms = app.get("platforms")
        screenshots = app.get("screenshots")
        achievements = app.get("achievements")
        background = app.get("background")
        background_raw = app.get("background_raw")

        if pc_requirements != None and len(pc_requirements) != 0:
            minimum = pc_requirements.get("minimum")
            recommended = pc_requirements.get("recommended")
            pc_requirements = (minimum, recommended)
        else:
            pc_requirements = None

        if mac_requirements != None and len(mac_requirements) != 0:
            minimum = mac_requirements.get("minimum")
            recommended = mac_requirements.get("recommended")
            mac_requirements = (minimum, recommended)
        else:
            mac_requirements = None

        if linux_requirements != None and len(linux_requirements) != 0:
            minimum = linux_requirements.get("minimum")
            recommended = linux_requirements.get("recommended")
            linux_requirements = (minimum, recommended)
        else:
            linux_requirements = None

        if price_overview != None:
            currency = price_overview.get("currency")
            initial = price_overview.get("initial")
            final = price_overview.get("final")
            discount_percent = price_overview.get("discount_percent")
            initial_formatted = price_overview.get("initial_formatted")
            final_formatted = price_overview.get("final_formatted")
            price_overview = (currency, initial, final, discount_percent, initial_formatted, final_formatted)

        # if achievements != None:
        #     total = achievements.get("total")
        #     if total != None or total != 0:
        #         highlighted = achievements.get("highlighted")
        #         if highlighted != None:
        #             achievements = (total, [(h.get("name"), h.get("path")) for h in highlighted])


        if screenshots != None:
            screenshots = [(scr.get("id"), scr.get("path_thumbnail"), scr.get("path_full")) for scr in screenshots]

        if platforms != None:
            windows = platforms.get("windows")
            mac = platforms.get("mac")
            linux = platforms.get("linux")
            platforms = (windows, mac, linux)
        
        if categories != None:
            categories = [ctg.get("id") for ctg in categories]
            self.__manager.add_app_ctg(steam_appid, categories)

        if genres != None:
            genres = [tag.get("description") for tag in genres]
            self.__manager.add_app_tag(steam_appid, genres, self.__tags)

        return (
            steam_appid, 
            name, 
            _type, 
            required_age, 
            is_free, 
            detailed_description, 
            about_the_game, 
            short_description,
            supported_languages, 
            header_image, 
            website, 
            pc_requirements, 
            mac_requirements, 
            linux_requirements, 
            legal_notice,
            developers, 
            publishers, 
            price_overview, 
            platforms, 
            screenshots,
            # achievements,
            background, 
            background_raw,
            )

    async def __async_fetch_app_details(self, session: ClientSession, appid: int):
        url = "https://store.steampowered.com/api/appdetails"
        params = {"appids": appid}
        try:
            async with session.get(url, timeout=60, params=params) as response:
                response = await response.json()
        except Exception as e:
            print(e)
            pass
        else:
            if response != None:
                response = tuple(response.values())[0]
                status = response.get('success')
                if status:
                    data = response.get('data')
                    if data == None:
                        return
                    return response.get('data')
            return
        return

    async def __async_fetch_apps_details(self, appids: list):
        tasks = []
        async with ClientSession() as session:
            for appid in appids:
                task = asyncio.ensure_future(self.__async_fetch_app_details(session, appid))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)
        result = []
        for resp in responses:
            if resp != None:
                result.append(self.__get_app_field_values(resp))
        return result

    def get_apps(self, count: int, step=3, id_start=0):
        apps_raw = get("https://api.steampowered.com/ISteamApps/GetAppList/v2/").json()\
        .get('applist')\
        .get('apps')

        appids = []
        for app_raw in apps_raw:
            if app_raw.get('name') == "":
                pass
            else:
                appids.append(app_raw.get('appid'))

        del apps_raw
        appids.sort()
        
        try:
            i_start = appids.index(id_start)
        except ValueError:
            i_start = 0
        
        appids = appids[i_start+1:i_start+1+count]
        bar = tqdm(total=ceil(len(appids)/step), position=0, leave=True, bar_format='{l_bar}{bar:20}{r_bar}{bar:-10b}')
        apps = []
        try:
            loop = asyncio.get_event_loop()
            for start in range(0, len(appids), step):
                task = asyncio.ensure_future(
                    self.__async_fetch_apps_details(appids[start: start + step])
                )
                loop.run_until_complete(task)
                res = task.result()
                apps.extend(res)
                time.sleep(1)
                bar.set_postfix_str({'Apps': len(apps)})
                bar.update()
        except KeyboardInterrupt:
            pass
        
        bar.close()
        return apps, self.labels
