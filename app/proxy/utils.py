import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


def is_proxy_usable(proxy):
    test_url = "https://httpbin.org/ip"
    try:
        response = requests.get(test_url, proxies={"http": proxy, "https": proxy}, timeout=10)
        response.raise_for_status()
        return proxy, True
    except requests.RequestException as e:
        print(f"Proxy {proxy} is not usable: {e}")
        return proxy, False


def validate_proxies_concurrently(proxies):
    results = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_proxy = {executor.submit(is_proxy_usable, proxy): proxy for proxy in proxies}
        for future in as_completed(future_to_proxy):
            proxy, is_usable = future.result()
            results.append({"proxy_url": proxy, "is_usable": is_usable})

    return results
