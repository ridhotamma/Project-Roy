import random

class ProxyRotator:
    def __init__(self, proxies):
        self.proxies = proxies
    
    def get_random_proxy(self):
        if not self.proxies:
            raise ValueError("Proxy list is empty")
        return random.choice(self.proxies)
