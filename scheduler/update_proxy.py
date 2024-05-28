import schedule
import time
import logging

from proxy import ProxyManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def job():
    proxy_manager = ProxyManager()
    try:
        proxy_manager.fetch_and_update_global_proxies()
        logging.info("Successfully updated global proxy list.")
    except Exception as e:
        logging.error(f"Error occurred during proxy update: {e}")

def start_background_update():
    schedule.every(6).hours.do(job)
    logging.info("Scheduled job to update proxy list every 6 hours.")

    logging.info("Running the first update immediately.")
    job()

    while True:
        schedule.run_pending()
        time.sleep(1)
