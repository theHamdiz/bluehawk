# Blue Hawk By Ahmad Hamdi Emara

import requests
import re
from collections import deque
import urllib.parse
import requests.exceptions
from bs4 import BeautifulSoup


def colorize(text, color):
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }
    return colors[color] + text + colors['reset']


def ensure_http_protocol(url):
    if not url.startswith(("http://", "https://")):
        # Assume http if not specified, but you can implement more advanced logic here
        return "http://" + url
    return url


print('\033[91mB\033[92mL\033[93mU\033[94mE\033[95m \033[96mH\033[91mA\033[92mW\033[93mK\033[0m')


class BlueHawk:
    def __init__(self, target_url, max_depth=100):

        self.target_url = ensure_http_protocol(target_url)

        self.max_depth = max_depth
        self.urls = deque([self.target_url])
        self.scraped_urls = set()
        self.emails = set()
    print('''
    ____     __    __  __    ______           __  __    ___  _       __    __ __
   / __ )   / /   / / / /   / ____/          / / / /   /   || |     / /   / //_/
  / __  |  / /   / / / /   / __/            / /_/ /   / /| || | /| / /   / ,<   
 / /_/ /  / /___/ /_/ /   / /___           / __  /   / ___ || |/ |/ /   / /| |  
/_____/  /_____/\____/   /_____/          /_/ /_/   /_/  |_||__/|__/   /_/ |_|  
                                                                                
    ''')

    def scrape(self):
        count = 0
        try:
            while len(self.urls):
                try:
                    count += 1
                    if count == self.max_depth:
                        break
                    url = self.urls.popleft()
                    self.scraped_urls.add(url)

                    parts = urllib.parse.urlsplit(url)
                    base_url = '{0.scheme}://{0.netloc}'.format(parts)
                    path = url[:url.rfind('/')+1] if '/' in parts.path else url

                    print(colorize('[%d] Processing %s' %
                                   (count, url), 'blue', True))

                    try:
                        response = requests.get(url)
                    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                        continue

                    new_emails = set(re.findall(
                        r"[a-z0-9\.\-\+_]+@[a-z0-9\.\-\+_]+\.[a-z]+", response.text, re.I))
                    self.emails.update(new_emails)

                    soup = BeautifulSoup(response.text, features="lxml")

                    for anchor in soup.find_all("a"):
                        link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
                        if link.startswith('/'):
                            link = base_url + link
                        elif not link.startswith('http'):
                            link = path + link
                        if not link in self.urls and not link in self.scraped_urls:
                            self.urls.append(link)
                except:
                    continue

        except KeyboardInterrupt:
            print(colorize('[-] Closing!', 'red', True))

    def display_emails(self):
        for mail in sorted(self.emails):
            print(colorize(mail, 'green', True))

    @staticmethod
    def identify():
        return "Blue Hawk By Ahmad Hamdi Emara"


def colorize(text, color, bold=False):
    colors = {
        'blue': '\033[94m',
        'green': '\033[92m',
        'red': '\033[91m'
    }
    end_color = '\033[0m'
    bold_code = '\033[1m' if bold else ''
    return f"{colors[color]}{bold_code}{text}{end_color}"


def main():
    depth_input = input(colorize(
        '[+] Enter Scrape Depth (Default is 100): ', 'blue', True))
    max_depth = int(depth_input) if depth_input.isdigit() else 100
    blue_hawk = BlueHawk(target_url=input(colorize(
        '[+] Enter Target URL To Scan: ', 'blue', True)), max_depth=max_depth)
    print(blue_hawk.identify())
    blue_hawk.scrape()
    blue_hawk.display_emails()


if __name__ == "__main__":
    main()
