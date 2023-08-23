"""
Blue Hawk By Ahmad Hamdi Emara - Email Scraper Framework
Version: 1.0.0
Author: Ahmad Hamdi Emara
Website: https://hamdiz.me
Copyright () 2023, Ahmad Hamdi Emara, All rights reserved.
"""

from helper import *

from bs4 import BeautifulSoup
import requests.exceptions
import urllib.parse
import re
import requests


class BlueHawk:
    def __init__(self, target_url, max_depth=0, mode=ScrapeMode.SMART):
        self.target_url = ensure_http_protocol(target_url)
        self.max_depth = max_depth
        self.urls = deque([self.target_url])
        self.scraped_urls = set()
        self.emails = set()
        self.mode = mode
        self.regex_config = RegexConfig()
        self.print_banner()
        self.counter = 0

    def print_banner(self):
        print(f'''
    ____     __    __  __    ______           __  __    ___  _       __    __ __
   / __ )   / /   / / / /   / ____/          / / / /   /   || |     / /   / //_/
  / __  |  / /   / / / /   / __/            / /_/ /   / /| || | /| / /   / ,<   
 / /_/ /  / /___/ /_/ /   / /___           / __  /   / ___ || |/ |/ /   / /| |  
/_____/  /_____/\____/   /_____/          /_/ /_/   /_/  |_||__/|__/   /_/ |_|  
                                                                                
    {self._identify()}
    ''')

    def scrape(self):
        self.counter = 0
        try:
            while len(self.urls):
                try:
                    self.counter += 1
                    if self._check_exit_conditions():
                        break
                    url = self.urls.popleft()
                    self.scraped_urls.add(url)
                    print(colorize('🔥[%d] Processing %s' % (
                        self.counter, self._truncate(url, 50)), 'yellow', True))
                    response = self._get_response(url)
                    if response:
                        self._process_response(response, url)
                except:
                    self.counter -= 1
                    continue

        except KeyboardInterrupt:
            print(colorize('\n[-] Closing Session!', 'red', True))
            sys.exit(1)
        except Exception as e:
            print(f"\nError encountered: {e}")

    def _check_exit_conditions(self):
        if (self.mode == ScrapeMode.LAZY and self.counter > 1) or ((self.mode == ScrapeMode.SMART or self.mode == ScrapeMode.VERBOSE) and self.counter > self.max_depth + 1):
            return True

        return False

    def _print_success_message(self):
        self.print_banner()
        print(
            f"🥰 Gathered {len(self.emails)} emails, thanks for your patience 🙏")

    def _get_base_url_and_path(self, url):
        parts = urllib.parse.urlsplit(url)
        base_url = '{0.scheme}://{0.netloc}'.format(parts)
        path = url[:url.rfind('/')+1] if '/' in parts.path else url
        return base_url, path

    def _get_response(self, url):
        try:
            return requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            return None

    def _process_response(self, response, url):
        new_emails = set(re.findall(
            self.regex_config.pattern, response.text, re.I))
        self.emails.update(new_emails)
        soup = BeautifulSoup(response.text, features="lxml")
        base_url, path = self._get_base_url_and_path(url)
        for anchor in soup.find_all("a"):
            self._process_anchor(anchor, base_url, path)
        if not new_emails:
            self._handle_no_emails_found()
            self.urls.appendleft(url)

    def _process_anchor(self, anchor, base_url, path):
        link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
        if link.startswith('/'):
            link = base_url + link
        elif not link.startswith('http'):
            link = path + link
        if link not in self.urls and link not in self.scraped_urls:
            self.urls.append(link)

    def _handle_no_emails_found(self):
        if self.regex_config.change_pattern():
            print(colorize(
                '😢[-] No emails found with the current regex pattern. Trying a different pattern...', 'red'))
            self.counter = 0
        else:
            print(
                colorize('❌[-] No emails found with any regex patterns. Exiting...', 'red'))

    def _truncate(self, text, max_length):
        if len(text) > max_length:
            return s[:max_length-3] + "..."
        return text

    def _get_domain(self, url: str) -> str:
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc
        domain = domain.split("www.")[-1]
        return domain

    def _save_emails_to_file(self):
        domain_name = self._get_domain(self.target_url)
        with open(f"{domain_name}.txt", "w") as file:
            for email in self.emails:
                file.write(email + "\n")
        print(f"Emails saved to {domain_name}.txt")

    def _display_emails(self):
        if len(self.emails) < 1:
            print(f"❌ {colorize('[-] No emails Found!', 'red', True)}")
        for mail in sorted(self.emails):
            print(f"✅ {colorize(mail, 'cyan', True)}")

    def end(self):
        self._print_success_message()
        self._display_emails()
        self._save_emails_to_file()

    @staticmethod
    def _identify():
        return colorize("Blue Hawk By Ahmad Hamdi Emara", 'magenta', True)


def main():
    try:
        parser = argparse.ArgumentParser(
            description="Blue Hawk - A Web Scraper By Ahmad Hamdi Emara")

        parser.add_argument("-d", "--domain", type=str,
                            help="Target domain (URL) to scan.")
        parser.add_argument("-m", "--mode", type=str, choices=["lazy", "smart", "verbose"], default="smart",
                            help="Scraping mode (lazy, smart, verbose). Default is verbose.")
        parser.add_argument("-l", "--max-depth", type=int, default=10,
                            help="Maximum depth to scrape. Default is 10.")

        domain, max_depth, mode = None, None, None
        # Check if the script is launched without any parameters or with positional parameters
        if len(sys.argv) < 2:
            domain = input(
                colorize('👉 [+] Enter Target URL To Scan: ', 'blue', True))
            depth_input = input(
                colorize('👉 [+] Enter Scrape Depth (Default is 10): ', 'blue', True))
            mode_input = input(
                colorize('👉 [+] Enter Scraping Mode (lazy, smart, verbose) 👉 (Default is smart): ', 'blue', True))
            max_depth = int(depth_input) if depth_input.isdigit() else 10
            mode = mode_input.lower() if mode_input in [
                "lazy", "smart", "verbose"] else "smart"
            print(f"{depth_input.isdigit()}, {depth_input}, {max_depth}")
        else:
            args = parser.parse_args()
            if not args.domain:
                parser.print_help()
                return
            domain = args.domain
            max_depth = args.max_depth
            mode = args.mode.lower()

        print(
            f"🔥 Gathering Emails On {domain} Using a max depth of {max_depth} in the {mode} mode 🥰")
        # Map string mode to ScrapeMode Enum
        mode_mapping = {
            "lazy": ScrapeMode.LAZY,
            "smart": ScrapeMode.SMART,
            "verbose": ScrapeMode.VERBOSE
        }
        selected_mode = mode_mapping[mode]

        blue_hawk = BlueHawk(
            target_url=domain, max_depth=max_depth, mode=selected_mode)
        blue_hawk.scrape()
        blue_hawk.end()
    except KeyboardInterrupt:
        print(colorize('\n[-] Closing Session!', 'red', True))
        exit(1)
    except Exception as e:
        print(
            colorize('\n[-] Fatal Error Happened, Terminating!', 'red', True))
        exit(2)


if __name__ == "__main__":
    main()
