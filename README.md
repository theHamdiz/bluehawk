## Blue Hawk - Information Gathering Tool

- Version: 1.0.0
- Author: Ahmad Hamdi Emara
- Website: https://hamdiz.me
- Copyright: © 2023, Ahmad Hamdi Emara, All rights reserved.
  
---

![](resources/Blue%20Hawk.png)

### Description:
`Blue Hawk` 🦅 is a powerful **information-gathering tool**  
designed to efficiently extract *email addresses*, *phone numbers* & *social links* from a given target website.  
Built with `Python`, it provides various features and scraping modes
for an optimized and user-friendly experience.

---

### Dependencies:
- BeautifulSoup
- requests
- *(Note: The script will automatically handle the installation of required packages.)*

### Usage:
- Clone the repository or download the bh.py and helper.py scripts.

---

#### There are two ways to run the script 👇

#### 1. Run the script using command-line arguments: 👇
```zsh
python3 bh.py -d [TARGET_URL] [OPTIONS]
```
- Replace `[TARGET_URL]` with the website URL from which you wish to scrape.
- Replace `[OPTIONS]` with Scraping modes (`--mode`) or their initials, as well as (`--max-depth`).
---

### Options:

`--max-depth` `[DEPTH]`: Set the maximum depth for scraping (**default is 10**).  
`--mode` `[MODE]`: Choose the scraping mode. Modes include:  
---
`SMART`: Intelligent Scraping.  
`LAZY`: One-Request Only Snapshot Scraping.  
`VERBOSE`: Recursively Scrape The Original Domain With Any Backlinks Contained Within. 
---

#### 2. Run the script without any command-line arguments:
##### Just run it as follows and it will ask you for input. 👇
```zsh
python3 bh.py
```
#### For detailed help:

```zsh
python3 bh.py --help
```

---

### Credits:
All credit goes to Ahmad Hamdi Emara for creating and maintaining this tool.  
Visit the official website for more tools and projects by the author.

