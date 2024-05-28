from proxy import ProxyManager, ProxyRotator
from scheduler import start_background_update

proxy_manager = ProxyManager()
proxies = proxy_manager.get_proxies(limit=10, region='US')

proxy_rotator = ProxyRotator(proxies=proxies)
rotated_ip = proxy_rotator.get_random_proxy()

start_background_update()

print(rotated_ip)
