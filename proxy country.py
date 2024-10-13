import requests

# Function to get country from an IP address using ipinfo.io API
def get_country_from_ip(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        
        if 'country' in data:
            return data['country']
        else:
            return "Unknown Country"
    except Exception as e:
        return f"Error: {e}"

# Function to read proxy IPs from a file and get countries
def get_proxy_countries(file_path):
    with open(file_path, 'r') as file:
        proxies = file.readlines()

    proxy_info = {}
    for proxy in proxies:
        # Extract the IP portion (remove ports if included, assuming format ip:port)
        ip = proxy.split(":")[0].strip()
        country = get_country_from_ip(ip)
        proxy_info[ip] = country
    
    return proxy_info

# Path to the file containing the list of proxies (one per line)
file_path = 'proxies.txt'  # Update this with the actual file path

# Get the countries for the proxies
proxy_country_map = get_proxy_countries(file_path)

# Print the result
for proxy, country in proxy_country_map.items():
    print(f"Proxy: {proxy}, Country: {country}")

