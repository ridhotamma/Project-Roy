import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


def read_proxy_list(file_path):
    with open(file_path, 'r') as file:
        proxies = file.readlines()
    return [f'http://{proxy.strip()}' for proxy in proxies]


def make_request(url, proxy=None):
    try:
        if proxy:
            response = requests.get(
                url, proxies={'http': proxy, 'https': proxy})
        else:
            response = requests.get(url)

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed {e}")
        return None


def is_proxy_usable(proxy):
    test_url = "https://httpbin.org/ip"  # Simple API to test the proxy
    try:
        response = requests.get(
            test_url, proxies={"http": proxy, "https": proxy}, timeout=10)
        response.raise_for_status()
        return proxy, True
    except requests.RequestException as e:
        print(f"Proxy {proxy} is not usable: {e}")
        return proxy, False


def validate_proxies_concurrently(proxies):
    usable_proxies = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_proxy = {executor.submit(
            is_proxy_usable, proxy): proxy for proxy in proxies}
        for future in as_completed(future_to_proxy):
            proxy, is_usable = future.result()
            if is_usable:
                usable_proxies.append(proxy)

    return usable_proxies
