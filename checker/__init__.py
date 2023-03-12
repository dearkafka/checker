#!/usr/bin/env python

import argparse
import configparser
import logging
import os
import random
import sys
import time

import telebot
from autoscraper import AutoScraper
from tinydb import Query, TinyDB

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("config_file", help="path to config file")
parser.add_argument("--debug", action="store_true", help="Enable debug logging")

args = parser.parse_args()

if args.debug:
    logging.getLogger().setLevel(logging.DEBUG)
else:
    logging.getLogger().setLevel(logging.INFO)

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

# Read config file
config = configparser.ConfigParser()
config.read(args.config_file)

# Set up scraper
scraper_url = config["Scraper"]["url"]
wanted_list = [url for url in config["WantedList"].values()]
scraper_file = config["File"]["scraper_file"]
scraper = AutoScraper()
if os.path.isfile(scraper_file):
    scraper.load(scraper_file)
else:
    scraper.build(scraper_url, wanted_list, text_fuzz_ratio=0.9)
    scraper.save(scraper_file)


# Set up time-related parameters
startup_delay_sec = int(config["Time"].get("startup_delay_sec", 10))
min_run_delay_sec = int(config["Time"].get("min_run_delay_min", 10)) * 60
max_run_delay_sec = int(config["Time"].get("max_run_delay_min", 30)) * 60
min_error_delay_sec = int(config["Time"].get("min_error_delay_min", 4)) * 60
max_error_delay_sec = int(config["Time"].get("max_error_delay_min", 12)) * 60


def send_telegram_message(message):
    bot = telebot.TeleBot(config["Telegram"]["bot_token"])
    if isinstance(message, str):
        message = [message]
    for m in message:
        bot.send_message(config["Telegram"]["chat_id"], m)
        time.sleep(10)


def check_db(result):
    db_filename = config["Database"]["database_file"]
    db = TinyDB(db_filename)
    query = Query()
    for item in result:
        if not db.search(query.url == item):
            db.insert({"url": item})
            send_telegram_message(item)


def main():
    i = 0
    send_telegram_message(config["Telegram"]["startup_message"])
    time.sleep(startup_delay_sec)
    while True:
        try:
            logging.info(f"Run {i}")
            result = scraper.get_result_similar(scraper_url)
            check_db(result)
            logging.debug(f"Have {result}")
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            time.sleep(random.randint(min_error_delay_sec, max_error_delay_sec))
        else:
            time.sleep(random.randint(min_run_delay_sec, max_run_delay_sec))
        i += 1


if __name__ == "__main__":
    main()
