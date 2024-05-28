from instabot import Bot
from proxy import ProxyManager, ProxyRotator
import requests

proxy_manager = ProxyManager()
proxies = proxy_manager.get_proxies(limit=15)

proxy_rotator = ProxyRotator(proxies=proxies)

def post_to_instagram_with_rotation(username, password, image_path, caption):
    proxy = proxy_rotator.get_random_proxy()
    proxies = {
        'http': proxy,
        'https': proxy
    }

    session = requests.Session()
    session.proxies.update(proxies)

    bot = Bot()
    bot.login(username=username, password=password)

    bot.upload_photo(image_path, caption=caption)
