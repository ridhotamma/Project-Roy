import re
import os
import requests
class ProxyManager:
    def __init__(self):
        pass

    def get_proxies(self, limit, region='GLOBAL'):
        base_directory = './data'
        filename = f'proxy-list-{region}.txt'
        filepath = os.path.join(base_directory, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f'No proxy list found for region: {region}')
        
        with open(filepath, 'r') as file:
            data = file.readlines()

        cleaned_data = self._clean_data(data)
        return cleaned_data[:limit]

    def _clean_data(self, data):
        ip_port_pattern = re.compile(r'(\b(?:\d{1,3}\.){3}\d{1,3}\b):(\d+)')
        ip_addresses = [match.group(0) for entry in data if (match := ip_port_pattern.search(entry))]
        return ip_addresses
    
    def fetch_and_update_global_proxies(self):
        url = "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
        response = requests.get(url)
        
        if response.status_code == 200:
            proxy_data = response.text.splitlines()
            cleaned_data = self._clean_data(proxy_data)

            with open(self.global_proxy_file, 'w') as file:
                for proxy in cleaned_data:
                    file.write(f"{proxy}\n")
            print("Updated global proxy list.")
        else:
            print("Failed to fetch proxy data.")
