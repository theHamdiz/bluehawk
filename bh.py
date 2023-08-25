"""
Blue Hawk By Ahmad Hamdi Emara - Information Gathering Tool
Version: 1.0.0
Author: Ahmad Hamdi Emara
Website: https://hamdiz.me
Copyright () 2023, Ahmad Hamdi Emara, All rights reserved.
"""

from helper import *
import os
from bs4 import BeautifulSoup
import requests.exceptions
import urllib.parse
import re
import csv


class BlueHawk:
    def __init__(self, target_url, max_depth=10, mode=ScrapeMode.SMART):
        self.target_url = ensure_http_protocol(target_url)
        self.max_depth = max_depth
        self.urls = deque([self.target_url])
        self.scraped_urls = set()
        self.emails = set()
        self.user_names = set()
        self.phone_numbers = set()
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
        while len(self.urls):
            self.counter += 1
            if self._check_exit_conditions():
                break
            url = self.urls.popleft()
            self.scraped_urls.add(url)
            print(colorize(
                f'🔥[{self.counter}] Processing {self._truncate(url, 50)}', 'yellow', True))
            response = None
            if (self.mode in [ScrapeMode.SMART, ScrapeMode.LAZY] and self._get_domain(
                    self.target_url) == self._get_domain(url)) or self.mode == ScrapeMode.VERBOSE:
                response = self._get_response(url)
            else:
                # If the link was a link outside the boundaries of the domain and the user is not using Verbose mode!
                self.counter -= 1
                print(colorize("👉[-] Skipping, use verbose mode if you want to go outside the boundaries "
                               "of the current domain!", 'red', False))
                continue
            if response:
                self._process_response(response, url)

    def _check_exit_conditions(self):
        if ((self.mode == ScrapeMode.LAZY and self.counter > 1) or ((
                self.mode == ScrapeMode.SMART or self.mode == ScrapeMode.VERBOSE) and self.counter > self.max_depth + 1)):  # Adding one here for good measure.
            return True

        return False

    @staticmethod
    def _get_base_url_and_path(url):
        parts = urllib.parse.urlsplit(url)
        base_url = '{0.scheme}://{0.netloc}'.format(parts)
        path = url[:url.rfind('/') + 1] if '/' in parts.path else url
        return base_url, path

    @staticmethod
    def _get_response(url):
        try:
            return requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            return None

    def _process_response(self, response, url):
        """
        Processes the html response from the server,
        Depending on the mode used checks for embedded links
        And adds them to the list of urls to scan, keeping the loop 
        in the scrape method going on, and for each link it processes
        it tries to capture emails, phone numbers and later on usernames
        """
        new_emails = set(re.findall(
            self.regex_config.pattern, response.text, re.I))
        new_phones = self._clean_phone_numbers(
            set(re.findall(self.regex_config.phone_regex, response.text, re.I)))

        self.phone_numbers.update(new_phones)
        self.emails.update(new_emails)

        soup = BeautifulSoup(response.text, features="lxml")
        base_url, path = self._get_base_url_and_path(url)
        # Get more links here.
        if not self.mode == ScrapeMode.LAZY:
            for anchor in soup.find_all("a"):
                self._process_anchor(anchor, base_url, path)
        # Here we are checking for found  emails.
        if not new_emails:
            # If they're directly visible in the HTML, We check mailto links.
            new_emails = set(re.findall(
                self.regex_config.mailto_regex, response.text, re.I))
            self.emails.update(new_emails)

    def _process_anchor(self, anchor, base_url, path):
        """
        This is the method that processes embedded links in any web page.
        It tries to unify the structure of the link depending on whether
        The link is relative or absolute!
        """
        link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
        path = path.replace('#', '')
        if link.startswith('/'):
            link = base_url + link
        elif not link.startswith('http'):
            link = path + '#' + link if not path.endswith('#') else path + link

        if link not in self.urls and link not in self.scraped_urls:
            self.urls.append(link)
            user_names = self._filter_and_construct_links(
                set(re.findall(self.regex_config.username_regex, link, re.I)))
            self.user_names.update(user_names)

    @staticmethod
    def _truncate(text: str, max_length: int) -> str:
        if len(text) > max_length:
            return text[:max_length - 3] + "..."
        return text

    @staticmethod
    def _get_domain(url: str) -> str:
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc
        domain = domain.split("www.")[-1]
        return domain

    def _display_emails(self) -> None:
        if len(self.emails) >= 1:
            print("Emails found:\n")
            for mail in sorted(self.emails):
                print(f"✅ {colorize(mail, 'cyan', True)}")
            print(colorize("=-" * 50, 'yellow', True))

    @staticmethod
    def _filter_and_construct_links(results) -> set:
        """
        Removes share links and other links that usually
        don't contain usernames or pages.
        """
        # Regular routes that are not usernames
        non_user_routes = {'in', 'p', 'sharer', 'intent',
                           'channel', 'shareArticle', 'reel', 'share', 'add', 'c'}

        # Filter out results with non-user routes
        filtered_results = {(platform, route) for platform,
                            route in results if route not in non_user_routes}

        # Construct platform links without 'https://www.'
        links = {f"{platform}/{route}" for platform, route in filtered_results}

        return links

    def _display_user_names(self) -> None:
        if len(self.user_names) >= 1:
            print("Usernames found:\n")
            for username in sorted(self.user_names):
                print(f"✅ {colorize(username, 'blue', True)}")
            print(colorize("=-" * 50, 'yellow', True))

    @staticmethod
    def _clean_phone_numbers(numbers: set) -> set:
        """
        Standardize numbers in a unified template.
        """
        # I know one-liners are not easy to understand;
        # But I just felt like implementing it this way.
        return {('+' + n[6:] if n.startswith('tel:00') else ('+966' + n[1:] if n.startswith('0') else n[4:])) for n in
                numbers}

    def _display_phone_numbers(self) -> None:
        if len(self.phone_numbers) >= 1:
            print(colorize("=-" * 50, 'yellow', True))
            print("Phone Numbers Found:\n")
            for number in sorted(self.phone_numbers):
                print(f"☎️ {colorize(number, 'magenta', True)}")
            print(colorize("=-" * 50, 'yellow', True))

    def _display_results(self) -> None:
        print(colorize("=-" * 50, 'yellow', True))
        print(
            f"✅ Found [{len(self.phone_numbers)}] Phone Number(s), [{len(self.emails)}] Email(s) and [{len(self.user_names)}] Username(s)")
        self._display_phone_numbers()
        self._display_emails()
        self._display_user_names()

    def _filter_results(self) -> None:
        """
            Final Check on email results to remove false positives.
        """
        extensions = (".png", ".webp", ".jpg", ".jpeg", ".tiff", ".gif")
        emails_to_remove = {email for email in self.emails if str(
            email).endswith(extensions)}

        self.emails -= emails_to_remove

    def _save_results(self) -> None:
        """
        For each result type (email, phone number, username)
        It creates a csv file containing the data for that type
        Only if the result is not empty.
        Its also responsible for creating a folder for each website scraped.
        """
        # I know one-liners through list-comprehension are hard to understand;
        # but I felt like I should do it that way.
        os.makedirs(os.path.join("output", self._get_domain(self.target_url)), exist_ok=True), [csv.writer(
            open(os.path.join("output", self._get_domain(self.target_url), f"{desc}.csv"), "w", newline='')).writerows(
            [[item] for item in s]) for s, desc in
            zip([sorted(self.phone_numbers), sorted(self.emails), sorted(self.user_names)],
                ["phones", "emails", "usernames"]) if s], print(
            colorize("🔥[+] Results saved!", "green", True))

    def end(self) -> None:
        self._filter_results()
        self._display_results()
        self._save_results()

    @staticmethod
    def _identify() -> str:
        return colorize("Blue Hawk By Ahmad Hamdi Emara", 'magenta', True)


def main():
    try:
        parser = argparse.ArgumentParser(
            description="Blue Hawk - A Web Scraper By Ahmad Hamdi Emara")

        parser.add_argument("-d", "--domain", type=str,
                            help="Target domain (URL) to scan.")
        parser.add_argument("-m", "--mode", type=str, choices=["lazy", "smart", "verbose"], default="smart",
                            help="Scraping mode (lazy, smart, verbose). Default is smart.")
        parser.add_argument("-l", "--max-depth", type=int, default=10,
                            help="Maximum depth (Limit) to scrape. Default is 10.")

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
            # Accept either the full mode name or the letter initials for it.
            modes = {
                "l": "lazy",
                "s": "smart",
                "v": "verbose"
            }

            mode_input_lower = mode_input.lower() if mode_input != "" else "smart"
            mode = modes.get(mode_input_lower[0], "smart") if mode_input_lower in modes.values(
            ) or mode_input_lower[0] in modes.keys() else "smart"

        else:
            args = parser.parse_args()
            if not args.domain:
                parser.print_help()
                return
            domain = args.domain
            max_depth = args.max_depth
            mode = args.mode.lower()

        print(
            f"🔥 Gathering Data On {domain} Using a max depth of {max_depth} in the {mode} mode 🥰")
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
            colorize(f'\n[-] Fatal Error Happened, Terminating!\n{e}', 'red', True))
        exit(2)


if __name__ == "__main__":
    main()
