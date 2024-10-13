import requests
import re
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor
import os

# Expanded list of proxy websites to scrape from
proxy_urls = [
    'https://www.sslproxies.org/',
    'https://free-proxy-list.net/',
    'https://www.us-proxy.org/',
    'https://www.socks-proxy.net/',
    'https://spys.me/proxy.txt',
    'https://www.proxy-list.download/api/v1/get?type=https',
    'https://www.proxy-list.download/api/v1/get?type=socks5',
    'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
    'https://multiproxy.org/txt_all/proxy.txt',


     ]

# Regular expression to match IP:PORT format
proxy_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+'

proxies = []
live_proxies = {}
dead_proxies = []

# Scrape proxies from multiple sources
for url in proxy_urls:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.text
            found_proxies = re.findall(proxy_pattern, content)
            proxies += found_proxies
            print(f"Scraped {len(found_proxies)} proxies from {url}")
        else:
            print(f"Failed to access {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error scraping {url}: {e}")

print(f"Total proxies scraped: {len(proxies)}")

# Function to get proxy country using IP-API
def get_proxy_country(ip):
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}')
        data = response.json()
        if data['status'] == 'success':
            return data['country']
        else:
            return "Unknown"
    except Exception:
        return "Unknown"

# Proxy checker function with country identification
def check_proxy(proxy):
    proxy_parts = proxy.split(':')
    proxy_ip = proxy_parts[0]
    proxy_port = proxy_parts[1]
    proxy_url = f'http://{proxy_ip}:{proxy_port}'

    try:
        # Test proxy by trying to access Google
        response = requests.get('https://www.google.com', proxies={"http": proxy_url, "https": proxy_url}, timeout=10)
        if response.status_code == 200:
            country = get_proxy_country(proxy_ip)
            print(colored(f"{proxy} - LIVE - {country}", 'green'))
            
            if country not in live_proxies:
                live_proxies[country] = []
            live_proxies[country].append(proxy)
        else:
            print(colored(f"{proxy} - DEAD (Invalid response)", 'red'))
            dead_proxies.append(proxy)
    except Exception:
        print(colored(f"{proxy} - DEAD (Connection failed)", 'red'))
        dead_proxies.append(proxy)

# Check proxies concurrently with ThreadPoolExecutor
if proxies:
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(check_proxy, proxies)

    # Save live proxies by country
    if live_proxies:
        for country, proxies_list in live_proxies.items():
            filename = f'proxies_{country.replace(" ", "_")}.txt'
            with open(filename, 'w') as live_file:
                for proxy in proxies_list:
                    live_file.write(proxy + '\n')
            print(f"Live proxies for {country} saved to {filename}.")

    # Save dead proxies to a file
    if dead_proxies:
        with open('deadproxy.txt', 'w') as dead_file:
            for proxy in dead_proxies:
                dead_file.write(proxy + '\n')
        print(f"Dead proxies saved to deadproxy.txt ({len(dead_proxies)} dead proxies).")
else:
    print("No proxies found after scraping.")
