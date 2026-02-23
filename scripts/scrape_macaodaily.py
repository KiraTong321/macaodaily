import argparse
import sys
from datetime import datetime, date as date_class
from pathlib import Path
from urllib.parse import urljoin
import re
import requests
from bs4 import BeautifulSoup

vendor_path = Path('libs/site-packages').resolve()
if vendor_path.exists():
    sys.path.insert(0, str(vendor_path))

parser = argparse.ArgumentParser(
    description='Fetch Macao Daily front page and economy section titles for a given date.'
)
parser.add_argument(
    'date',
    nargs='?',
    help='Target date in YYYY-MM-DD format; defaults to today if omitted.',
)
args = parser.parse_args()


def parse_date(value: str) -> date_class:
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError as exc:
        raise SystemExit(f'Date must be YYYY-MM-DD, got {value}') from exc


target_date = parse_date(args.date) if args.date else date_class.today()
root_url = f'https://www.macaodaily.com/html/{target_date:%Y-%m}/{target_date:%d}/node_2.htm'


def extract_titles(soup):
    seen = set()
    result = []
    for a in soup.find_all('a', href=lambda h: h and h.startswith('content')):
        text = a.get_text(strip=True)
        if text and text not in seen:
            seen.add(text)
            result.append(text)
    return result


def fetch_page(url):
    resp = requests.get(url, timeout=10)
    resp.encoding = 'utf-8'
    return BeautifulSoup(resp.text, 'html.parser')


root_soup = fetch_page(root_url)

head_titles = extract_titles(root_soup)
print('頭版標題:')
for title in head_titles:
    print(title)
print()

econ_title_prefix = chr(0x7B2C)
econ_title_mid = chr(0x7248)
econ_title_colon = chr(0xFF1A)
econ_title_econ = chr(0x7D93) + chr(0x6FDF)
econ_pattern = re.compile(
    f'^{econ_title_prefix}[A-Z][0-9]+{econ_title_mid}{econ_title_colon}{econ_title_econ}$'
)
econ_links = []
for a in root_soup.find_all(
    'a', string=lambda text: text and econ_pattern.match(text.strip())
):
    href = a.get('href')
    if href:
        econ_links.append((a.get_text(strip=True), urljoin(root_url, href)))

for name, href in econ_links:
    section_label = name.replace('\uff1a', ': ')
    econ_soup = fetch_page(href)
    econ_titles = extract_titles(econ_soup)
    if not econ_titles:
        continue
    print(section_label)
    for title in econ_titles:
        print(title)
    print()
