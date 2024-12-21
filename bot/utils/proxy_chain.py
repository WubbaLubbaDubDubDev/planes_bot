import json
import os


class ProxyChain:
    def __init__(self, proxies_file: str, sessions_workdir: str, load_proxies_from_json: bool = True):
        self.proxies = []
        self.used_proxies = set()
        self.proxies_file = proxies_file
        self.sessions_workdir = sessions_workdir
        self.load_proxies_from_txt()
        if load_proxies_from_json:
            self.load_proxies_from_json()

    def load_proxies_from_json(self):
        file_path = os.path.join(self.sessions_workdir, 'bindings.json')
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
                for entry in data:
                    if 'proxy' in entry:
                        proxy = entry['proxy']
                        if proxy in self.proxies:
                            self.used_proxies.add(proxy)

    def load_proxies_from_txt(self):
        with open(self.proxies_file, 'r') as file:
            self.proxies.extend(line.strip() for line in file if line.strip())
        if len(self.proxies) == 0:
            raise ValueError("The proxy list is empty.")

    def get_next_proxy(self):
        for proxy in self.proxies:
            if proxy not in self.used_proxies:
                self.used_proxies.add(proxy)
                return proxy
        self.used_proxies.clear()
        return self.get_next_proxy()
