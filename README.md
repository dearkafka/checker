![checker](https://socialify.git.ci/dearkafka/checker/image?description=1&descriptionEditable=Blazingly%20simple%20any%20website%20scrape%2C%20compare%20with%20db%2C%20notify%20in%20Telegram%20&font=Jost&language=1&name=1&owner=1&pattern=Plus&theme=Light)
# Checker

Checker is a Python package that checks websites for new items and sends notifications via Telegram.

## Installation

To install Checker, you can use pip:

```
pip install git+https://github.com/dearkafka/checker.git
```

This will install Checker and its dependencies.

## Usage

Checker is designed to be used as a command-line tool. After installing the package, you can run the `checker` command to check for new items:

```
checker path/to/config.ini
```

Here, `path/to/config.ini` is the path to a configuration file that Checker uses to determine which website to scrape and how to send notifications. The configuration file should be in the INI format, see [example](.config.ini); with sections and keys defined as follows:

```
[Scraper]
url = https://example.com/
```

The `[Scraper]` section specifies the URL of the website to scrape.

```
[WantedList]
url1 = https://example.com/item1
url2 = https://example.com/item2
```

Before anything, you need to train scraper.  
The `[WantedList]` section lists the URLs of the items from the `[Scraper]` so that simiar items would be recognised in future. It's like a training data for scraper and it's what you would like to receive if you scraped manually. You can add as many items as you like, using keys numbered from `url1` to `urln`.

```
[File]
scraper_file = scraper.json
```

The `[File]` section specifies the filename to use for the scraper cache/scrape model file. This file will store the results of previous scrapes, so that Checker can determine whether there are new items.

```
[Telegram]
bot_token = YOUR_BOT_TOKEN
chat_id = YOUR_CHAT_ID
startup_message = Hello!
```

The `[Telegram]` section specifies the Telegram bot token and chat ID to use for sending notifications. You can obtain a bot token by talking to the BotFather in Telegram. The chat ID can be obtained by sending a message to your bot and inspecting the `chat` object in the JSON response. The `startup_message` key specifies a message to send when the Checker is started.

```
[Time]
startup_delay_sec = 10
min_run_delay_min = 10
max_run_delay_min = 30
min_error_delay_min = 4
max_error_delay_min = 12
```

The `[Time]` section specifies the time-related parameters for the Checker. The `startup_delay_sec` key specifies the number of seconds to wait before starting the first scrape. The `min_run_delay_min` and `max_run_delay_min` keys specify the minimum and maximum number of minutes to wait between scrapes. The `min_error_delay_min` and `max_error_delay_min` keys specify the minimum and maximum number of minutes to wait before retrying a scrape in case of an error.

Checker provides only new data using very convenient tinyDB so it wont send same twice to your Telegram.

## systemd Service

Checker can also be set up as a systemd service on Linux. This allows it to run in the background and automatically start at boot time.

To create the systemd service, run the following command:

```
checker-service --create path/to/config.ini
```

This will create a new systemd service called `checker.service` that uses the specified configuration file. It will start immediately.

## Debug Logging

If you want to enable debug logging for Checker, you can pass the `--debug` flag when running the `checker` command:

```
checker --debug path/to/config.ini
```

This will output more detailed log messages to specified log file (stated in config.ini)


## License
The project is licensed under the Cooperative Non-Violent Public License v7 or later (CNPLv7+) - see the [LICENSE](LICENSE) for details. Built for people, not corporations.
