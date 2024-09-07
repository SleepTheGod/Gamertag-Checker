#!/bin/bash

sudo apt-get install proxychains

# Input and output files
INPUT_FILE="list.txt"
OUTPUT_FILE="make.txt"
PROXY_LIST="proxies.txt"

# Clear output file
> "$OUTPUT_FILE"
> "$PROXY_LIST"

# Fetch the list of proxies from ProxyScrape
echo "Fetching proxies..."
curl -s "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=HTTP" -o "$PROXY_LIST"

# Get the first five proxies
head -n 5 "$PROXY_LIST" > selected_proxies.txt

# Function to check gamertag availability
check_gamertag() {
    local gamertag="$1"
    local url="https://account.xbox.com/en-us/Profile?gamertag=$gamertag"
    local proxy
    
    # Loop through the selected proxies
    while IFS= read -r proxy; do
        echo "Checking gamertag: $gamertag using proxy: $proxy"
        
        # Making the request via the current proxy
        response=$(curl -s -x "$proxy" "$url")

        if echo "$response" | grep -q "We could not find that gamertag"; then
            echo "$gamertag" >> "$OUTPUT_FILE"
            echo "Gamertag '$gamertag' is available."
            return
        fi
    done < selected_proxies.txt

    echo "Gamertag '$gamertag' is taken or an error occurred."
}

# Read from input file and check each gamertag
while IFS= read -r gamertag; do
    check_gamertag "$gamertag"
done < "$INPUT_FILE"

echo "Gamertag availability check completed. Available gamertags are listed in '$OUTPUT_FILE'."
