import requests

# Input and output files
input_file = "list.txt"
output_file = "make.txt"
proxy_list_file = "proxies.txt"
selected_proxies_file = "selected_proxies.txt"

# Function to test proxy validity
def is_proxy_valid(proxy):
    test_url = "https://httpbin.org/ip"
    proxies_dict = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    try:
        response = requests.get(test_url, proxies=proxies_dict, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Fetch the list of proxies from ProxyScrape
print("Fetching proxies...")
response = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all")
with open(proxy_list_file, "w") as f:
    f.write(response.text)

# Filter valid proxies and save them
with open(proxy_list_file, "r") as f:
    all_proxies = f.readlines()

valid_proxies = []
for proxy in all_proxies:
    proxy = proxy.strip()
    if is_proxy_valid(proxy):
        valid_proxies.append(proxy)
        print(f"Proxy {proxy} is valid.")

with open(selected_proxies_file, "w") as f:
    for proxy in valid_proxies[:5]:  # Save only the first 5 valid proxies
        f.write(f"{proxy}\n")

# Function to check gamertag availability
def check_gamertag(gamertag):
    url = f"https://account.xbox.com/en-us/Profile?gamertag={gamertag}"
    
    # Loop through the selected proxies
    with open(selected_proxies_file, "r") as f:
        proxies = f.readlines()

    for proxy in proxies:
        proxy = proxy.strip()
        proxies_dict = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        print(f"Checking gamertag: {gamertag} using proxy: {proxy}")

        try:
            response = requests.get(url, proxies=proxies_dict, timeout=10)

            if "We could not find that gamertag" in response.text:
                with open(output_file, "a") as output:
                    output.write(f"{gamertag}\n")
                print(f"Gamertag '{gamertag}' is available.")
                return
        except requests.RequestException as e:
            print(f"Error using proxy {proxy}: {e}")

    print(f"Gamertag '{gamertag}' is taken or an error occurred.")

# Read from input file and check each gamertag
try:
    with open(input_file, "r") as f:
        gamertags = f.readlines()

    for gamertag in gamertags:
        gamertag = gamertag.strip()
        check_gamertag(gamertag)

    print(f"Gamertag availability check completed. Available gamertags are listed in '{output_file}'.")

except FileNotFoundError:
    print(f"Input file {input_file} not found!")
