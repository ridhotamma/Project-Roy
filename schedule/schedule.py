import schedule
import time
from proxy import ProxyManager

def job():
    proxy_manager = ProxyManager()
    proxy_manager.fetch_and_update_global_proxies()

def init():
    schedule.every(6).hours.do(job)

    job()

    while True:
        schedule.run_pending()
        time.sleep(1)
