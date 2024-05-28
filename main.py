from proxy import ProxyManager, ProxyRotator
from automation.instagram.like_post import like_instagram_post

proxy_manager = ProxyManager()
proxies = proxy_manager.get_proxies(limit=10, region='US')

proxy_rotator = ProxyRotator(proxies=proxies)
rotated_ip = proxy_rotator.get_random_proxy()

like_instagram_post('ridhotamma', '******', 'https://www.instagram.com/p/C7gGL-tSpUZ/')
