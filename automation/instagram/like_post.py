from instabot import Bot
from proxy import ProxyManager, ProxyRotator
import requests

proxy_manager = ProxyManager()
proxies = proxy_manager.get_proxies(limit=10, region='US')

proxy_rotator = ProxyRotator(proxies=proxies)

def like_instagram_post(username, password, post_url):
    proxy = proxy_rotator.get_random_proxy()
    proxies = {
        'http': proxy,
        'https': proxy
    }

    session = requests.Session()
    session.proxies.update(proxies)

    bot = Bot()
    bot.login(username=username, password=password)

    media_id = bot.get_media_id_from_link(post_url)
    
    bot.like(media_id)
