import requests

def check_proxy(proxy):
    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}',
    }
    try:
        response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=5)
        if response.status_code == 200:
            return True
    except:
        pass
    return False

def get_country(ip):
    try:
        response = requests.get(f'https://ipapi.co/{ip}/country/')
        if response.status_code == 200:
            return response.text.strip()
    except:
        pass
    return None

def main():
    with open('proxies.txt', 'r') as file:
        proxies = file.read().splitlines()

    us_proxies = []

    for proxy in proxies:
        if check_proxy(proxy):
            ip = proxy.split(':')[0]
            country_code = get_country(ip)
            if country_code == 'US':
                us_proxies.append(proxy)
                print(f'Live US proxy found: {proxy}')
            else:
                print(f'Live proxy from other country: {proxy} ({country_code})')
        else:
            print(f'Dead proxy: {proxy}')

    # Save only live US proxies
    with open('US_proxies.txt', 'w') as us_file:
        for proxy in us_proxies:
            us_file.write(f'{proxy}\n')

if __name__ == '__main__':
    main()
