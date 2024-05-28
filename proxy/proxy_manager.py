import re
import os
import requests

class ProxyManager:
    def __init__(self):
        self.base_directory = './data'
        if not os.path.exists(self.base_directory):
            os.makedirs(self.base_directory)

    def get_proxies(self, limit, region='GLOBAL'):
        filename = f'proxy-list-{region}.txt'
        filepath = os.path.join(self.base_directory, filename)
        
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

        filename = f'proxy-list-GLOBAL.txt'
        filepath = os.path.join(self.base_directory, filename)

        if response.status_code == 200:
            proxy_data = response.text.splitlines()
            cleaned_data = self._clean_data(proxy_data)

            with open(filepath, 'w') as file:
                for proxy in cleaned_data:
                    file.write(f"{proxy}\n")
                    
            print("Updated global proxy list.")
        else:
            print("Failed to fetch proxy data.")
