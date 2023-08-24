"""
Blue Hawk By Ahmad Hamdi Emara - Email Scraper Framework
Version: 1.0.0
Author: Ahmad Hamdi Emara
Website: https://hamdiz.me
Copyright () 2023, Ahmad Hamdi Emara, All rights reserved.
"""

# Install dependencies

import subprocess
from dataclasses import dataclass
from enum import Enum
from collections import deque
import argparse
import sys

import requests

installed_a_package = False


def install_package(package):
    """Install a Python package using pip."""
    subprocess.check_call(["pip", "install", package])
    global installed_a_package
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
    # If the URL already starts with http or https, return as is.
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


@dataclass
class RegexConfig:
    def __init__(self, pattern=None):
        self.pattern = self.regex_all_emails if pattern is None else pattern

    emails_but_not_photos = (r"[a-zA-Z0-9\.\-\+_]+@[a-zA-Z0-9\.\-\+_]+\.(?!(jpg|jpeg|png|gif|tiff|heic|bmp|webp)$)["
                             r"a-zA-Z]+")
    regex_all_emails = r"[a-zA-Z0-9\.\-\+_]+@[a-zA-Z0-9\.\-\+_]+\.[a-zA-Z]+"
    regex_simple_general = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"
    regex_stricter = r"\b[A-Za-z0-9._%+-]+@(?![A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b)[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    mailto_regex = r'mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    phone_regex = r'tel:(?:\+|00(?!0))\d{1,3}[\s]?\d{10,13}|^0\d{9}$|^9200\s?\d{5}$'
    username_regex = (r'https?://(?:www\.)?(facebook\.com|twitter\.com|instagram\.com|linkedin\.com|x\.com|youtube\.com'
                      r'|tiktok\.com|snapchat\.com)/([^/\s?]+)')

    all_patterns = [regex_stricter, emails_but_not_photos, regex_simple_general,
                    mailto_regex, regex_all_emails]

