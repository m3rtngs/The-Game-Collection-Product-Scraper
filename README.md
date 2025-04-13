Scraping The Game Collection Website
===================================================

<p align="center">
  <img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg" alt="made-with-python">
  <img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat" alt="contributions welcome">
</p>

<p align="center">
  <a href="#about">About</a> •
  <a href="#features">Features</a> •
  <a href="#usage">Usage</a> •
  <a href="#configuration">Configuration</a>
</p>

## About
This project is a Python script that scrapes the [The Game Collection](https://www.thegamecollection.net/) website to find and notify you about the availability of a specific product, in this case, the "Pokemon TCG" game collection. It uses the BeautifulSoup library to parse the HTML content and the Discord Webhook API to send notifications to a specified Discord channel.

## Features
- Scrapes the The Game Collection website to find the specified product
- Sends a Discord webhook notification when the product is found
- Keeps track of previously found products to avoid duplicate notifications
- Configurable search query, total results, and batch size

## Usage
1. Clone the repository:
   ```
   git clone https://github.com/your-username/game-collection-scraper.git
   ```
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure the script by modifying the `config.ini` file:
   - `query`: The search query to use (e.g., "Pokemon TCG")
   - `totalResults`: The total number of results to fetch
   - `batchSize`: The number of results to fetch per request
   - `Discord Webhook URL`: Add the Discord Webhook URL where you want the notifications to be sent
4. Run the script:
   ```
   python main.py
   ```

## Configuration
The configuration for the script is stored in the `config.ini` file. You can modify the following settings:

- `query`: The search query to use for the scraping process.
- `totalResults`: The total number of results to fetch from the website.
- `batchSize`: The number of results to fetch per request.
- `Discord Webhook URL`: The URL of the Discord Webhook where the notifications will be sent.
