# CCN - The Game Collection Scraper
# Made by m3rtngs

import configparser
import requests
import json
import re
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed

# Read configuration
config = configparser.ConfigParser()
config.read('config.ini')

query = config.get('DEFAULT', 'query')
query = query.replace(' ', '%20') #Replace spaces with %20 to make sure URL request does not fail

headers = {
    "Referer": "https://www.thegamecollection.net/",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

while True:
    # Initial variables for pagination
    total_results = int(config.get('DEFAULT', 'totalResults'))  # Total results to fetch
    batch_size = int(config.get('DEFAULT', 'batchSize'))    # Number of results to fetch per request
    results = []        # List to store all results
    current_offset = 0  # Start offset

    while current_offset < total_results:
        # Create the query URL with limit and offset
        queryURL = f'https://dynamic.sooqr.com/suggest/script/?type=suggest&searchQuery={query}&filterInitiated=false&triggerFilter=&triggerFilterValue=&triggerFilterIndex=&filtersShowAll=false&enableFiltersShowAll=false&securedFiltersHash=false&sortBy=0&offset={current_offset}&limit={batch_size}&requestIndex=4&locale=en_GB&url=%2F&sid=106194053.1618324852.1743425556.1743425556.1743425556.1&index=magento%3A18647&view=a904165fcb8fb44f&account=SQ-118647-1&_=1743426968497'
        
        # Make the request
        html = requests.get(queryURL, headers=headers)
        
        # Use regex to extract the JSON payload
        json_match = re.search(r'sendSearchQueryByScriptCompleted\((.*)\)', html.text)
        if json_match:
            json_data = json_match.group(1)  # Get the capturing group
            parsed_data = json.loads(json_data)  # Parse the JSON string
            
            # Access the resultsPanel HTML
            html_content = parsed_data.get("resultsPanel", {}).get("html", "")
            
            # Parse the HTML using Beautiful Soup
            soup = BeautifulSoup(html_content, "html.parser")
            batch_results = soup.find_all("div", class_="sqr-resultItem")
            
            # Store the results
            results.extend(batch_results)
            
            # Increase the offset for the next batch of results
            current_offset += batch_size

        else:
            print("No JSON data found in the response.")
            break

    # Extract and print titles, images, and prices for all results
    print(f"Total results retrieved: {len(results)}")

    webhook = DiscordWebhook(
        url = "", #Add Discord Webhook URL here
        rate_limit_retry=True
    )

    for result in results:
        found = False
        title_tag = result.find("a", rel="title")
        title = title_tag["title"] if title_tag else "No title available"
        price_tag = result.find("div", class_="sqr-price")
        price = price_tag.text if price_tag else "No price available"
        image_tag = result.find("img")
        image = image_tag["src"] if image_tag else "No image available"
        href = title_tag["href"] if title_tag else "No link available"

        with open('found.txt', 'a+') as foundFile:
            foundFile.seek(0)  
            for eachLine in foundFile:
                if eachLine.strip() == title:
                    found = True
                    break

            if not found:
                foundFile.write(title + '\n')
                print(f'Found: {title}')

        if found:
            continue

        embed = DiscordEmbed(
            title=title,
            description="Stock detected on The Game Collection.",
            color="03b2f8"
        )
        embed.add_embed_field(
            name = "Price",
            value = str(price)
        )
        embed.add_embed_field(
            name = 'URL:',
            value = f'[Click Here]({href})'
        )
        embed.set_thumbnail(url=image)
        webhook.add_embed(embed)
        
        response = webhook.execute()
        webhook.embeds.clear()