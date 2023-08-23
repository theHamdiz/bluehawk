## Blue Hawk - Email Scraper Framework

```bash
   ____     __    __  __    ______           __  __    ___  _       __    __ __
   / __ )   / /   / / / /   / ____/          / / / /   /   || |     / /   / //_/
  / __  |  / /   / / / /   / __/            / /_/ /   / /| || | /| / /   / ,<   
 / /_/ /  / /___/ /_/ /   / /___           / __  /   / ___ || |/ |/ /   / /| |  
/_____/  /_____/\____/   /_____/          /_/ /_/   /_/  |_||__/|__/   /_/ |_|  
            
```
---

- Version: 1.0.0
- Author: Ahmad Hamdi Emara
- Website: https://hamdiz.me
- Copyright: © 2023, Ahmad Hamdi Emara, All rights reserved.
---
### Description:
Blue Hawk is a powerful email scraping framework designed to efficiently extract email addresses from a given target website. Built with Python, it provides various features and scraping modes for an optimized and user-friendly experience.
---
### Dependencies:
- BeautifulSoup
- requests
*(Note: The script will automatically handle the installation of required packages.)*

### Usage:
-- Clone the repository or download the bh.py and helper.py scripts.

---

#### Run the script using:
```zsh
python bh.py -d [TARGET_URL] [OPTIONS]
```
-Replace [TARGET_URL] with the website URL from which you wish to scrape emails.

---

### Options:

--max-depth [DEPTH]: Set the maximum depth for scraping (default is 0).
--mode [MODE]: Choose the scraping mode. Modes include:
SMART: Intelligent scraping.
... (additional modes can be listed here).

---

For detailed help:

```zsh
python bh.py --help
```

---

### Credits:
All credit goes to Ahmad Hamdi Emara for creating and maintaining this tool. Visit the official website for more tools and projects by the author.

