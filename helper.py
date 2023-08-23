"""
Blue Hawk By Ahmad Hamdi Emara - Email Scraper Framework
Version: 1.0.0
Author: Ahmad Hamdi Emara
Website: https://hamdiz.me
Copyright () 2023, Ahmad Hamdi Emara, All rights reserved.
"""

# Install dependencies

import subprocess
from enum import Enum
from collections import deque
import argparse
import sys

installed_a_package = False


def install_package(package_name):
    """Install a Python package using pip."""
    subprocess.check_call(["pip", "install", package_name])
    installed_a_package = True


# List of modules and their corresponding pip package names
modules_to_check = {
    'requests': 'requests',
    'urllib.parse': None,  # part of the standard library, no need to install
    'bs4': 'beautifulsoup4',
}

for module, package_name in modules_to_check.items():
    try:
        exec(f"import {module}")
    except ImportError:
        if package_name:
            print(f"{module} not found. Installing {package_name}...")
            install_package(package_name)
        else:
            print(
                f"Error: {module} is part of the standard library but couldn't be imported!")

if installed_a_package:
    print("All required modules are available.")


def colorize(text: str, color: str, bold=False) -> str:
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
    end_color = '\033[0m'
    bold_code = '\033[1m' if bold else ''
    return f"{colors[color]}{bold_code}{text}{end_color}"


def ensure_http_protocol(url: str) -> str:
    """
        Ensure the URL starts with an HTTP/HTTPS protocol. 
        If the website supports HTTPS, default to HTTPS.
    """
    # If the URL already starts with http or https, return as is
    if url.startswith(("http://", "https://")):
        return url

    # Try to connect with HTTPS, if successful return the HTTPS URL, otherwise default to HTTP
    https_url = "https://" + url
    try:
        response = requests.head(https_url, timeout=5)
        if response.status_code < 400:  # Check if the server responded with a successful status code
            return https_url
    except (requests.exceptions.MissingSchema,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout):
        pass

    # Default to HTTP
    return "http://" + url


class ScrapeMode(Enum):
    LAZY = 1
    SMART = 2
    VERBOSE = 3


class RegexConfig:
    def __init__(self, pattern=None):
        self.pattern = self.regex_all_emails if pattern is None else pattern

    regex_no_photos = r"(?<!.jpg|.jpeg|.png|.gif|.tiff|.bmp)[a-z0-9.-+_]+@[a-z0-9.-+_]+.[a-z]+"
    regex_all_emails = r"[a-z0-9\.\-\+_]+@[a-z0-9\.\-\+_]+\.[a-z]+"
    regex_simple_general = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    regex_stricter = r"\b[A-Za-z0-9._%+-]+@(?![A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b)[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    all_patterns = [regex_stricter, regex_all_emails,
                    regex_no_photos, regex_simple_general]

    def change_pattern(self) -> bool:
        for i, pattern in enumerate(self.all_patterns):
            if self.pattern == pattern:
                next_pattern_index = (i + 1) % len(self.all_patterns)
                self.pattern = self.all_patterns[next_pattern_index]
                return True
        return False
